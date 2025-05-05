import React, { useEffect, useState } from 'react';
import { Container, Typography, Paper, Button, Box, Switch, FormControlLabel } from '@mui/material';
import { api } from '../services/api';
import StudentTable from './StudentTable';
import ReportDialog from './ReportDialog';
import Filters from './StudentFilters';

export default function StudentRecords() {
    const [students, setStudents] = useState([]);
    const [selected, setSelected] = useState([]); // Stores the registered_no of selected students
    const [selectedStudentsData, setSelectedStudentsData] = useState([]); // Stores full student objects of selected students
    const [dialogOpen, setDialogOpen] = useState(false);
    const [showSelectedOnly, setShowSelectedOnly] = useState(false);

    useEffect(() => {
        api.fetchStudents()
            .then(res => {
                console.log("API Response:", res.data); // ✅ Confirm it's an array
                setStudents(res.data);
            })
            .catch(console.error);
    }, []);

    // Toggle selection of a student registration number
    const handleSelect = (regNo) => {
        const selectedStudent = students.find(s => s.registered_no === regNo);

        setSelected(prev =>
            prev.includes(regNo)
                ? prev.filter(id => id !== regNo)
                : [...prev, regNo]
        );

        setSelectedStudentsData(prev =>
            prev.some(s => s.registered_no === regNo)
                ? prev.filter(s => s.registered_no !== regNo)
                : [...prev, selectedStudent]
        );
    };

    const handleGenerate = ({ selected, reportType, pdfType, selected_columns }) => {
        if (reportType === 'excel') {
            api.generateExcelReport({
                selected_students: selected,
                selected_columns  // now correctly references the prop from the dialog
            });
        }
        else if (reportType === 'pdf') {
            api.generatePdfReport({
                selected_students: selected,
                generation_type: pdfType
            });
        }
        setDialogOpen(false);
    };

    const handleFilterChange = ({ branch, semester }) => {
        api.fetchStudents({
            ...(branch && { branch }),
            ...(semester && { curr_semester: semester })
        })
            .then(res => setStudents(res.data))
            .catch(console.error);
    };

    const handleSelectAll = () => {
        const allDisplayedIds = students.map(s => s.registered_no);

        setSelected(prev => [...new Set([...prev, ...allDisplayedIds])]);

        setSelectedStudentsData(prev => {
            const newStudents = students.filter(s => !prev.find(p => p.registered_no === s.registered_no));
            return [...prev, ...newStudents];
        });
    };

    // ✅ Deselect all students
    const handleClearSelection = () => {
        setSelected([]);
        setSelectedStudentsData([]);
    };

    // ✅ Display only selected students
    const displayedStudents = showSelectedOnly ? selectedStudentsData : students;

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Student Records
            </Typography>

            <Filters onFilterChange={handleFilterChange} />

            {/* ✅ Buttons and Toggle Controls */}
            <Box display="flex" gap={2} alignItems="center" mb={2}>
                <Button variant="outlined" onClick={handleSelectAll}>
                    Select All Displayed
                </Button>
                <Button variant="outlined" color="error" onClick={handleClearSelection}>
                    Clear Selection
                </Button>
                <FormControlLabel
                    control={
                        <Switch
                            checked={showSelectedOnly}
                            onChange={() => setShowSelectedOnly(prev => !prev)}
                        />
                    }
                    label="Show Selected Only"
                />
                <Typography variant="body2" color="text.secondary">
                    Selected: {selected.length}
                </Typography>
            </Box>

            <Paper>
                <StudentTable
                    students={displayedStudents} // ✅ only showing filtered students
                    selected={selected}
                    handleSelect={handleSelect}
                />
            </Paper>

            <Button
                variant="contained"
                sx={{ mt: 2 }}
                disabled={!selected.length}
                onClick={() => setDialogOpen(true)}
            >
                Generate Report for Selected Students
            </Button>

            <ReportDialog
                open={dialogOpen}
                onClose={() => setDialogOpen(false)}
                onGenerate={handleGenerate}
                selected={selected}
            />
        </Container>
    );
}
