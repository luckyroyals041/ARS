const express = require('express');
const router = express.Router();
const pool = require('../config/database');

// Get all achievements
router.get('/', async (req, res) => {
  try {
    const connection = await pool.getConnection();
    
    try {
      const [achievements] = await connection.query(`
        SELECT 
          id, 
          registration_number, 
          title, 
          description, 
          DATE_FORMAT(achievement_date, '%Y-%m-%d') as achievement_date, 
          category,
          scope,
          created_at, 
          updated_at 
        FROM achievements 
        ORDER BY achievement_date DESC
      `);
      
      res.json(achievements);
    } catch (error) {
      console.error('Database query error:', error);
      res.status(500).json({ 
        message: 'Database query error', 
        error: error.message 
      });
    } finally {
      connection.release();
    }
  } catch (error) {
    console.error('Database connection error:', error);
    res.status(500).json({ 
      message: 'Database connection error', 
      error: error.message 
    });
  }
});

// Get link status
router.get('/link-status', async (req, res) => {
  try {
    const connection = await pool.getConnection();
    
    try {
      const [rows] = await connection.query(
        "SELECT value FROM settings WHERE key_name = 'achievement_link_active'"
      );
      
      const isActive = rows.length > 0 ? rows[0].value === 'true' : true;
      res.json({ active: isActive });
    } catch (error) {
      console.error('Database query error:', error);
      res.status(500).json({ message: 'Error fetching link status', error: error.message });
    } finally {
      connection.release();
    }
  } catch (error) {
    console.error('Database connection error:', error);
    res.status(500).json({ message: 'Database connection error', error: error.message });
  }
});

// Update link status
router.post('/link-status', async (req, res) => {
  try {
    const { active } = req.body;
    
    if (active === undefined) {
      return res.status(400).json({ message: 'Missing active status' });
    }
    
    const connection = await pool.getConnection();
    
    try {
      await connection.query(
        "INSERT INTO settings (key_name, value) VALUES ('achievement_link_active', ?) " +
        "ON DUPLICATE KEY UPDATE value = ?",
        [active.toString(), active.toString()]
      );
      
      res.json({ message: 'Link status updated', active });
    } catch (error) {
      console.error('Database query error:', error);
      res.status(500).json({ message: 'Error updating link status', error: error.message });
    } finally {
      connection.release();
    }
  } catch (error) {
    console.error('Database error:', error);
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// POST a new achievement
router.post('/', async (req, res) => {
  try {
    const { registration_number, title, description, category, achievement_date, scope } = req.body;
    
    // Validate required fields
    if (!registration_number || !title || !category) {
      return res.status(400).json({ message: 'Missing required fields' });
    }
    
    const connection = await pool.getConnection();
    
    try {
      const [result] = await connection.query(`
        INSERT INTO achievements 
        (registration_number, title, description, category, achievement_date, scope)
        VALUES (?, ?, ?, ?, ?, ?)
      `, [registration_number, title, description, category, achievement_date, scope]);
      
      res.status(201).json({ 
        message: 'Achievement created successfully',
        id: result.insertId
      });
    } catch (error) {
      console.error('Database query error:', error);
      res.status(500).json({ 
        message: 'Database query error', 
        error: error.message 
      });
    } finally {
      connection.release();
    }
  } catch (error) {
    console.error('Error creating achievement:', error);
    res.status(500).json({ 
      message: 'Error creating achievement', 
      error: error.message 
    });
  }
});

module.exports = router;