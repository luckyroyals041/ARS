import React, { useEffect, useState } from 'react';
import {
    Container,
    Typography,
    Paper,
    Button,
    Box,
    Switch,
    FormControlLabel,
    Dialog,
    DialogTitle,
    DialogContent,
    IconButton
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import { api } from '../services/api';
import StudentTable from './StudentTable';
import ReportDialog from './ReportDialog';
import Filters from './StudentFilters';
import PdfViewer from './PdfViewer';

export default function StudentRecords() {
    const [students, setStudents] = useState([]);
    const [selected, setSelected] = useState([]);             // registered_no array
    const [selectedStudentsData, setSelectedStudentsData] = useState([]); // full objects
    const [dialogOpen, setDialogOpen] = useState(false);
    const [showSelectedOnly, setShowSelectedOnly] = useState(false);

    // PDF Viewer state
    const [viewerOpen, setViewerOpen] = useState(false);
    const [viewerUrl, setViewerUrl] = useState('');

    useEffect(() => {
        api.fetchStudents()
            .then(res => setStudents(res.data))
            .catch(console.error);
    }, []);

    const handleSelect = regNo => {
        const student = students.find(s => s.registered_no === regNo);
        setSelected(prev =>
            prev.includes(regNo) ? prev.filter(id => id !== regNo) : [...prev, regNo]
        );
        setSelectedStudentsData(prev =>
            prev.some(s => s.registered_no === regNo)
                ? prev.filter(s => s.registered_no !== regNo)
                : [...prev, student]
        );
    };

    const handleGenerate = ({ selected, reportType, pdfType, selected_columns }) => {
        if (reportType === 'excel') {
            api.generateExcelReport({ selected_students: selected, selected_columns });
        } else {
            api.generatePdfReport({ selected_students: selected, generation_type: pdfType });
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
        const ids = students.map(s => s.registered_no);
        setSelected(prev => Array.from(new Set([...prev, ...ids])));
        setSelectedStudentsData(prev => {
            const newOnes = students.filter(s => !prev.find(p => p.registered_no === s.registered_no));
            return [...prev, ...newOnes];
        });
    };

    const handleClearSelection = () => {
        setSelected([]);
        setSelectedStudentsData([]);
    };

    const displayedStudents = showSelectedOnly ? selectedStudentsData : students;

    // NEW: preview handler
    const handlePreview = regNo => {
        setViewerUrl(`${api.downloadIndividualReport(regNo)}`); // should be /download-pdf/:regNo or /preview-pdf/:regNo
        setViewerOpen(true);
    };

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Student Records
            </Typography>

            <Filters onFilterChange={handleFilterChange} />

            <Box display="flex" gap={2} alignItems="center" mb={2}>
                <Button variant="outlined" onClick={handleSelectAll}>Select All Displayed</Button>
                <Button variant="outlined" color="error" onClick={handleClearSelection}>Clear Selection</Button>
                <FormControlLabel
                    control={
                        <Switch
                            checked={showSelectedOnly}
                            onChange={() => setShowSelectedOnly(v => !v)}
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
                    students={displayedStudents}
                    selected={selected}
                    handleSelect={handleSelect}
                    handlePreview={handlePreview}   // pass preview handler down
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

            {/* PDF Preview Dialog */}
            <Dialog
                open={viewerOpen}
                onClose={() => setViewerOpen(false)}
                maxWidth="lg"
                fullWidth
            >
                <DialogTitle>
                    PDF Preview
                    <IconButton
                        aria-label="close"
                        onClick={() => setViewerOpen(false)}
                        sx={{ position: 'absolute', right: 8, top: 8 }}
                    >
                        <CloseIcon />
                    </IconButton>
                </DialogTitle>
                <DialogContent dividers>
                    {viewerUrl ? (
                        <PdfViewer src={viewerUrl} />
                    ) : (
                        <Typography>Loading...</Typography>
                    )}
                </DialogContent>
            </Dialog>
        </Container>
    );
}
