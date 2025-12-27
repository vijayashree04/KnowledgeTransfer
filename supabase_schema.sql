-- Supabase Database Schema for Knowledge Stream
-- Run this SQL in your Supabase SQL Editor to set up the database tables

-- Teams Table
CREATE TABLE IF NOT EXISTS teams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    access_code TEXT NOT NULL UNIQUE,
    team_lead_email TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    team_id UUID REFERENCES teams(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Documents Table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename TEXT NOT NULL,
    uploaded_by TEXT NOT NULL,
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    file_path TEXT NOT NULL,
    summary TEXT,
    content TEXT,
    upload_date TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_team_id ON users(team_id);
CREATE INDEX IF NOT EXISTS idx_teams_access_code ON teams(access_code);
CREATE INDEX IF NOT EXISTS idx_documents_team_id ON documents(team_id);
CREATE INDEX IF NOT EXISTS idx_documents_filename ON documents(filename);

-- Enable Row Level Security (RLS)
ALTER TABLE teams ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- RLS Policies for Teams
-- Allow all operations for now (you can restrict later based on your needs)
CREATE POLICY "Allow all operations on teams" ON teams
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- RLS Policies for Users
CREATE POLICY "Allow all operations on users" ON users
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- RLS Policies for Documents
CREATE POLICY "Allow all operations on documents" ON documents
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Note: These policies allow broad access. For production, you should restrict:
-- - Users should only see documents from their team
-- - Only team leads should be able to delete documents
-- - Users should only be able to update their own profile

