#!/bin/bash
echo "Setting up Faculty Dashboard database tables..."

# Database credentials
DB_USER="lucky"
DB_PASS="#Db@1234"
DB_NAME="reporting_system"

# Create faculty_student_mapping table if it doesn't exist
echo "Creating faculty_student_mapping table..."
mysql -u $DB_USER -p$DB_PASS $DB_NAME << EOF
CREATE TABLE IF NOT EXISTS faculty_student_mapping (
  id INT AUTO_INCREMENT PRIMARY KEY,
  faculty_id INT NOT NULL,
  student_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY unique_mapping (faculty_id, student_id)
);

-- Add sample data if table is empty
INSERT IGNORE INTO faculty_student_mapping (faculty_id, student_id)
SELECT 1, id FROM students LIMIT 50;
EOF

# Update certifications table to use registration_number
echo "Updating certifications table..."
mysql -u $DB_USER -p$DB_PASS $DB_NAME << EOF
-- Check if certifications table exists
CREATE TABLE IF NOT EXISTS certifications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  registration_number VARCHAR(20) NOT NULL,
  title VARCHAR(255) NOT NULL,
  issuing_organization VARCHAR(255),
  issue_date DATE,
  expiry_date DATE,
  credential_id VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (registration_number) REFERENCES students(registration_number)
);

-- Add sample certifications data
INSERT IGNORE INTO certifications (registration_number, title, issuing_organization, issue_date, expiry_date, credential_id)
SELECT 
  s.registration_number,
  CASE FLOOR(RAND() * 10)
    WHEN 0 THEN 'AWS Certified Developer'
    WHEN 1 THEN 'Microsoft Azure Fundamentals'
    WHEN 2 THEN 'Google Cloud Associate Engineer'
    WHEN 3 THEN 'Certified Kubernetes Administrator'
    WHEN 4 THEN 'Oracle Java Certification'
    WHEN 5 THEN 'Cisco CCNA'
    WHEN 6 THEN 'CompTIA Security+'
    WHEN 7 THEN 'MongoDB Certified Developer'
    WHEN 8 THEN 'Salesforce Administrator'
    ELSE 'Certified Ethical Hacker'
  END,
  CASE FLOOR(RAND() * 10)
    WHEN 0 THEN 'Amazon Web Services'
    WHEN 1 THEN 'Microsoft'
    WHEN 2 THEN 'Google'
    WHEN 3 THEN 'Cloud Native Computing Foundation'
    WHEN 4 THEN 'Oracle'
    WHEN 5 THEN 'Cisco'
    WHEN 6 THEN 'CompTIA'
    WHEN 7 THEN 'MongoDB Inc.'
    WHEN 8 THEN 'Salesforce'
    ELSE 'EC-Council'
  END,
  DATE_SUB(CURRENT_DATE, INTERVAL FLOOR(RAND() * 365) DAY),
  DATE_ADD(CURRENT_DATE, INTERVAL FLOOR(RAND() * 365) DAY),
  CONCAT('CERT-', UPPER(SUBSTRING(MD5(RAND()), 1, 8)))
FROM students s
JOIN faculty_student_mapping fsm ON s.id = fsm.student_id
WHERE fsm.faculty_id = 1
LIMIT 30;
EOF

# Add sample achievements data
echo "Adding sample achievements data..."
mysql -u $DB_USER -p$DB_PASS $DB_NAME << EOF
-- Check if achievements table exists
CREATE TABLE IF NOT EXISTS achievements (
  id INT AUTO_INCREMENT PRIMARY KEY,
  registration_number VARCHAR(20) NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  achievement_date DATE,
  category VARCHAR(50),
  scope VARCHAR(50) DEFAULT 'Inside the College',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (registration_number) REFERENCES students(registration_number)
);

-- Add sample achievements data
INSERT IGNORE INTO achievements (registration_number, title, description, achievement_date, category, scope)
SELECT 
  s.registration_number,
  CASE FLOOR(RAND() * 10)
    WHEN 0 THEN 'Won coding competition'
    WHEN 1 THEN 'Published research paper'
    WHEN 2 THEN 'Completed internship at Google'
    WHEN 3 THEN 'Hackathon winner'
    WHEN 4 THEN 'Best project award'
    WHEN 5 THEN 'Scholarship recipient'
    WHEN 6 THEN 'Sports achievement'
    WHEN 7 THEN 'Cultural event winner'
    WHEN 8 THEN 'Community service award'
    ELSE 'Academic excellence award'
  END,
  CONCAT('Achievement details for ', s.name),
  DATE_SUB(CURRENT_DATE, INTERVAL FLOOR(RAND() * 365) DAY),
  CASE FLOOR(RAND() * 5)
    WHEN 0 THEN 'Academic'
    WHEN 1 THEN 'Technical'
    WHEN 2 THEN 'Sports'
    WHEN 3 THEN 'Cultural'
    ELSE 'Community Service'
  END,
  CASE FLOOR(RAND() * 3)
    WHEN 0 THEN 'Inside the College'
    WHEN 1 THEN 'State Level'
    ELSE 'National Level'
  END
FROM students s
JOIN faculty_student_mapping fsm ON s.id = fsm.student_id
WHERE fsm.faculty_id = 1
LIMIT 45;
EOF

echo "Setup complete! Faculty Dashboard database tables are ready."
echo "You can now run ./run_all.sh to start the application."