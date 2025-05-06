import React from 'react';
import {
    Table, TableHead, TableRow, TableCell,
    TableBody, Checkbox, Button
} from '@mui/material';
import { api } from '../services/api';
import { tableColumns } from '../constants/columns';

export default function StudentTable({ students, selected, handleSelect, handlePreview }) {

    const handleIndividual = (regNo) => {
        const link = document.createElement('a');
        link.href = api.downloadIndividualReport(regNo);
        link.download = `${regNo}_report.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <Table>
            <TableHead>
                <TableRow>
                    <TableCell>Select</TableCell>
                    {tableColumns.map(col => <TableCell key={col}>{col}</TableCell>)}
                    <TableCell>Actions</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {Array.isArray(students) && students.map(s => (
                    <TableRow key={s.registered_no}>
                        <TableCell>
                            <Checkbox
                                checked={selected.includes(s.registered_no)}
                                onChange={() => handleSelect(s.registered_no)}
                            />
                        </TableCell>
                        <TableCell>{s.registered_no}</TableCell>
                        <TableCell>{s.name}</TableCell>
                        <TableCell>{s.branch}</TableCell>
                        <TableCell>{s.curr_semester}</TableCell>
                        <TableCell>
                            <Button
                                variant="contained" size="small" color="success"
                                onClick={() => handleIndividual(s.registered_no)}
                            >
                                Generate Report
                            </Button>
                            <Button
                                variant="outlined" size="small" sx={{ ml: 1 }}
                                onClick={() => handlePreview(s.registered_no)}
                            >
                                Preview
                            </Button>
                        </TableCell>

                    </TableRow>
                ))}
            </TableBody>
        </Table>
        

    );
}
