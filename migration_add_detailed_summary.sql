-- Migration: Add detailed_summary and summary_file_path columns to documents table
-- Run this SQL in your Supabase SQL Editor to add support for storing detailed summaries and summary files

ALTER TABLE documents 
ADD COLUMN IF NOT EXISTS detailed_summary TEXT;

ALTER TABLE documents 
ADD COLUMN IF NOT EXISTS summary_file_path TEXT;

-- Add comments to the columns
COMMENT ON COLUMN documents.detailed_summary IS 'Comprehensive detailed summary with headings, generated for document summaries tab';
COMMENT ON COLUMN documents.summary_file_path IS 'Path to the summarized document file stored in Supabase Storage';

