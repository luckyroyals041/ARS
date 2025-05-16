import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Chip
} from '@mui/material';
import { motion } from 'framer-motion';

// Icons
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import EventIcon from '@mui/icons-material/Event';
import PersonIcon from '@mui/icons-material/Person';
import SearchIcon from '@mui/icons-material/Search';
import WarningIcon from '@mui/icons-material/Warning';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

import { api } from '../../services/api_enhanced';

const CounselingNotes = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [students, setStudents] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState('');
  const [counselingSessions, setCounselingSessions] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [dialogMode, setDialogMode] = useState('add'); // 'add' or 'edit'
  const [selectedSession, setSelectedSession] = useState(null);
  const [formData, setFormData] = useState({
    student_id: '',
    session_date: '',
    notes: '',
    action_items: '',
    follow_up_date: '',
    status: 'pending'
  });

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        // In a real implementation, these would be actual API calls
        // For now, we'll use mock data
        
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Mock students data
        const mockStudents = [
          { id: 1, name: 'Akella Venkata', regNo: '22A91A6101', branch: 'AIML', semester: 6, cgpa: 8.7, status: 'Good' },
          { id: 2, name: 'Anusuri Bharathi', regNo: '22A91A6102', branch: 'AIML', semester: 6, cgpa: 9.2, status: 'Excellent' },
          { id: 3, name: 'Ari Naresh', regNo: '22A91A6103', branch: 'AIML', semester: 6, cgpa: 7.5, status: 'Good' },
          { id: 4, name: 'Arugollu Lalu Prasad', regNo: '22A91A6104', branch: 'AIML', semester: 6, cgpa: 6.8, status: 'Average' },
          { id: 5, name: 'Ayushi Singh', regNo: '22A91A6105', branch: 'AIML', semester: 6, cgpa: 4.9, status: 'At Risk' },
        ];
        
        // Mock counseling sessions
        const mockCounselingSessions = [
          { 
            id: 1, 
            student_id: 1, 
            student_name: 'Akella Venkata',
            session_date: '2024-05-10',
            notes: 'Discussed academic progress and career goals. Student is performing well in most subjects but needs improvement in Database Systems.',
            action_items: '1. Practice more database queries\n2. Join the database study group\n3. Complete the online course on SQL',
            follow_up_date: '2024-05-24',
            status: 'pending'
          },
          { 
            id: 2, 
            student_id: 2, 
            student_name: 'Anusuri Bharathi',
            session_date: '2024-05-08',
            notes: 'Excellent academic performance. Discussed research opportunities and internship possibilities.',
            action_items: '1. Apply for the summer research program\n2. Prepare resume for internship applications\n3. Work on the research proposal',
            follow_up_date: '2024-05-22',
            status: 'completed'
          },
          { 
            id: 3, 
            student_id: 5, 
            student_name: 'Ayushi Singh',
            session_date: '2024-05-05',
            notes: 'Student is struggling with multiple subjects. Discussed study strategies and additional support options.',
            action_items: '1. Attend remedial classes for Programming\n2. Meet with subject tutors weekly\n3. Create a structured study schedule',
            follow_up_date: '2024-05-15',
            status: 'pending'
          },
          { 
            id: 4, 
            student_id: 5, 
            student_name: 'Ayushi Singh',
            session_date: '2024-04-20',
            notes: 'Initial counseling session to address poor performance in mid-semester exams.',
            action_items: '1. Identify weak areas\n2. Create study plan\n3. Weekly progress reports',
            follow_up_date: '2024-05-05',
            status: 'completed'
          },
          { 
            id: 5, 
            student_id: 3, 
            student_name: 'Ari Naresh',
            session_date: '2024-04-15',
            notes: 'Discussed balancing academics with extracurricular activities. Student is active in sports but maintaining good grades.',
            action_items: '1. Create a balanced schedule\n2. Prioritize assignments\n3. Time management workshop',
            follow_up_date: '2024-05-15',
            status: 'pending'
          },
        ];
        
        setStudents(mockStudents);
        setCounselingSessions(mockCounselingSessions);
      } catch (error) {
        console.error("Error fetching data:", error);
        setError("Failed to load data. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleStudentChange = (event) => {
    setSelectedStudent(event.target.value);
  };

  const handleOpenAddDialog = () => {
    setDialogMode('add');
    setFormData({
      student_id: selectedStudent || '',
      session_date: new Date().toISOString().split('T')[0],
      notes: '',
      action_items: '',
      follow_up_date: '',
      status: 'pending'
    });
    setOpenDialog(true);
  };

  const handleOpenEditDialog = (session) => {
    setDialogMode('edit');
    setSelectedSession(session);
    setFormData({
      student_id: session.student_id,
      session_date: session.session_date,
      notes: session.notes,
      action_items: session.action_items,
      follow_up_date: session.follow_up_date,
      status: session.status
    });
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = () => {
    // In a real implementation, this would call the API
    if (dialogMode === 'add') {
      // Mock adding a new session
      const newSession = {
        id: counselingSessions.length + 1,
        ...formData,
        student_name: students.find(s => s.id === parseInt(formData.student_id))?.name || ''
      };
      setCounselingSessions(prev => [...prev, newSession]);
    } else {
      // Mock updating a session
      setCounselingSessions(prev => 
        prev.map(s => s.id === selectedSession.id ? { ...s, ...formData } : s)
      );
    }
    
    handleCloseDialog();
  };

  const handleDeleteSession = (id) => {
    // In a real implementation, this would call the API
    setCounselingSessions(prev => prev.filter(session => session.id !== id));
  };

  const handleMarkAsCompleted = (id) => {
    // In a real implementation, this would call the API
    setCounselingSessions(prev => 
      prev.map(session => 
        session.id === id ? { ...session, status: 'completed' } : session
      )
    );
  };

  // Filter sessions based on selected student
  const filteredSessions = selectedStudent 
    ? counselingSessions.filter(session => session.student_id === parseInt(selectedStudent))
    : counselingSessions;

  // Sort sessions by date (newest first)
  const sortedSessions = [...filteredSessions].sort((a, b) => 
    new Date(b.session_date) - new Date(a.session_date)
  );

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        when: "beforeChildren",
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold' }}>
          Counseling Notes
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Manage student counseling sessions and follow-ups
        </Typography>
      </Box>

      <motion.div variants={itemVariants}>
        <Paper sx={{ p: 3, mb: 3 }}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Select Student</InputLabel>
                <Select
                  value={selectedStudent}
                  onChange={handleStudentChange}
                  label="Select Student"
                  startAdornment={<PersonIcon sx={{ mr: 1 }} />}
                >
                  <MenuItem value="">All Students</MenuItem>
                  {students.map((student) => (
                    <MenuItem key={student.id} value={student.id}>
                      {student.name} ({student.regNo})
                      {student.status === 'At Risk' && (
                        <Chip 
                          label="At Risk" 
                          color="error" 
                          size="small" 
                          sx={{ ml: 1 }} 
                        />
                      )}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={6} sx={{ display: 'flex', justifyContent: 'flex-end' }}>
              <Button 
                variant="contained" 
                startIcon={<AddIcon />}
                onClick={handleOpenAddDialog}
                disabled={!selectedStudent && dialogMode === 'add'}
                sx={{
                  background: 'linear-gradient(45deg, #4568dc 30%, #b06ab3 90%)',
                }}
              >
                Add Counseling Session
              </Button>
            </Grid>
          </Grid>
        </Paper>
      </motion.div>

      <motion.div variants={itemVariants}>
        <Paper sx={{ p: 3 }}>
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              {selectedStudent 
                ? `Counseling Sessions for ${students.find(s => s.id === parseInt(selectedStudent))?.name}`
                : 'All Counseling Sessions'
              }
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {sortedSessions.length} session(s) found
            </Typography>
          </Box>
          
          {sortedSessions.length > 0 ? (
            <List>
              {sortedSessions.map((session) => (
                <Card key={session.id} sx={{ mb: 3 }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <EventIcon sx={{ mr: 1, color: 'primary.main' }} />
                        <Typography variant="subtitle1">
                          Session Date: {session.session_date}
                        </Typography>
                      </Box>
                      
                      <Chip 
                        label={session.status === 'completed' ? 'Completed' : 'Pending Follow-up'} 
                        color={session.status === 'completed' ? 'success' : 'warning'} 
                        size="small" 
                      />
                    </Box>
                    
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" color="text.secondary">
                        Student:
                      </Typography>
                      <Typography variant="body1">
                        {session.student_name}
                      </Typography>
                    </Box>
                    
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" color="text.secondary">
                        Notes:
                      </Typography>
                      <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                        {session.notes}
                      </Typography>
                    </Box>
                    
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" color="text.secondary">
                        Action Items:
                      </Typography>
                      <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                        {session.action_items}
                      </Typography>
                    </Box>
                    
                    <Box>
                      <Typography variant="subtitle2" color="text.secondary">
                        Follow-up Date:
                      </Typography>
                      <Typography variant="body1">
                        {session.follow_up_date}
                      </Typography>
                    </Box>
                    
                    <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
                      {session.status === 'pending' && (
                        <Button 
                          variant="outlined" 
                          color="success" 
                          startIcon={<CheckCircleIcon />} 
                          onClick={() => handleMarkAsCompleted(session.id)}
                          sx={{ mr: 1 }}
                        >
                          Mark as Completed
                        </Button>
                      )}
                      
                      <Button 
                        variant="outlined" 
                        startIcon={<EditIcon />} 
                        onClick={() => handleOpenEditDialog(session)}
                        sx={{ mr: 1 }}
                      >
                        Edit
                      </Button>
                      
                      <Button 
                        variant="outlined" 
                        color="error" 
                        startIcon={<DeleteIcon />} 
                        onClick={() => handleDeleteSession(session.id)}
                      >
                        Delete
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              ))}
            </List>
          ) : (
            <Alert severity="info">
              {selectedStudent 
                ? "No counseling sessions found for this student. Click 'Add Counseling Session' to create one."
                : "No counseling sessions found. Select a student and click 'Add Counseling Session' to create one."
              }
            </Alert>
          )}
        </Paper>
      </motion.div>

      {/* Add/Edit Counseling Session Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {dialogMode === 'add' ? 'Add New Counseling Session' : 'Edit Counseling Session'}
        </DialogTitle>
        
        <DialogContent dividers>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth margin="normal">
                <InputLabel>Student</InputLabel>
                <Select
                  name="student_id"
                  value={formData.student_id}
                  onChange={handleFormChange}
                  label="Student"
                  required
                  disabled={dialogMode === 'edit'}
                >
                  {students.map(student => (
                    <MenuItem key={student.id} value={student.id}>
                      {student.name} ({student.regNo})
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Session Date"
                name="session_date"
                type="date"
                value={formData.session_date}
                onChange={handleFormChange}
                margin="normal"
                InputLabelProps={{
                  shrink: true,
                }}
                required
              />
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Notes"
                name="notes"
                value={formData.notes}
                onChange={handleFormChange}
                margin="normal"
                multiline
                rows={4}
                required
                placeholder="Enter detailed notes about the counseling session..."
              />
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Action Items"
                name="action_items"
                value={formData.action_items}
                onChange={handleFormChange}
                margin="normal"
                multiline
                rows={3}
                placeholder="List action items, one per line..."
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Follow-up Date"
                name="follow_up_date"
                type="date"
                value={formData.follow_up_date}
                onChange={handleFormChange}
                margin="normal"
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <FormControl fullWidth margin="normal">
                <InputLabel>Status</InputLabel>
                <Select
                  name="status"
                  value={formData.status}
                  onChange={handleFormChange}
                  label="Status"
                >
                  <MenuItem value="pending">Pending Follow-up</MenuItem>
                  <MenuItem value="completed">Completed</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </DialogContent>
        
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button 
            onClick={handleSubmit} 
            variant="contained"
            color="primary"
            disabled={!formData.student_id || !formData.session_date || !formData.notes}
          >
            {dialogMode === 'add' ? 'Add Session' : 'Save Changes'}
          </Button>
        </DialogActions>
      </Dialog>
    </motion.div>
  );
};

export default CounselingNotes;