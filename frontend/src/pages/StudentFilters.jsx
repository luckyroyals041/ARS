// Filters.jsx
import React, { useState } from "react";
import { FormControl, InputLabel, MenuItem, Select, Box } from "@mui/material";

const branchMap = {
    AIML: "Artificial Intelligence And Machine Learning",
    CSE: "Computer Science and Engineering",
    IT: "Information Technology",
    ECE: "Electronics and Communication Engineering",
    EEE: "Electrical and Electronics Engineering",
    MECH: "Mechanical Engineering",
    CIVIL: "Civil Engineering",
};

export default function Filters({ onFilterChange }) {
    const [branch, setBranch] = useState("");
    const [semester, setSemester] = useState("");

    const handleBranchChange = (event) => {
        const value = event.target.value;
        setBranch(value);
        onFilterChange({
            branch: branchMap[value],
            semester,
        });
    };

    const handleSemesterChange = (event) => {
        const value = event.target.value;
        setSemester(value);
        onFilterChange({
            branch: branchMap[branch],
            semester: value,
        });
    };

    return (
        <Box display="flex" gap={2} mb={2}>
            <FormControl fullWidth>
                <InputLabel>Branch</InputLabel>
                <Select value={branch} onChange={handleBranchChange} label="Branch">
                    <MenuItem value=""><em>None</em></MenuItem>
                    {Object.keys(branchMap).map((code) => (
                        <MenuItem key={code} value={code}>{code}</MenuItem>
                    ))}
                </Select>
            </FormControl>

            <FormControl fullWidth>
                <InputLabel>Semester</InputLabel>
                <Select value={semester} onChange={handleSemesterChange} label="Semester">
                    <MenuItem value=""><em>None</em></MenuItem>
                    {[...Array(8)].map((_, i) => (
                        <MenuItem key={i + 1} value={i + 1}>{i + 1}</MenuItem>
                    ))}
                </Select>
            </FormControl>
        </Box>
    );
}
