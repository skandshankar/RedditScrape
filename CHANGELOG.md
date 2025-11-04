# Changelog

## [2.0.0] - 2025-11-04

### 🎯 Major Improvements

#### Code Structure & Organization
- **Refactored to function-based architecture** - Broke monolithic code into 8 well-defined functions
- **Added comprehensive docstrings** - Every function now has detailed documentation
- **Main execution wrapper** - Added `main()` function with proper entry point (`if __name__ == "__main__"`)
- **Removed unused imports** - Eliminated `pandas`, `datetime`, `subprocess`, and `sys` (not being used)

#### Error Handling & Validation
- **Added try-except blocks** throughout the code for robust error handling
- **Input validation** - Validates subreddit name, post limit (1-100), and user choices
- **Authentication testing** - Verifies Reddit login actually works before proceeding
- **Graceful failure handling** - Returns `None` on errors instead of crashing
- **Keyboard interrupt handling** - Properly catches Ctrl+C for clean exit

#### File Management
- **Fixed filename generation** - Now uses `{submission_id}_{sanitized_title}.mp3` instead of ugly `Submission(id='xyz').mp3`
- **Filename sanitization** - Added `sanitize_filename()` to remove invalid characters, limit length
- **Duplicate file detection** - Skips files that already exist
- **Auto-create output directory** - Creates `audio_output/` folder automatically
- **Cross-platform path handling** - Uses `os.path.join()` for compatibility

#### User Experience
- **Enhanced UI with visual feedback** - Added checkmarks (✓), crosses (✗), and warnings (⚠)
- **Progress indicators** - Shows `[1/10]`, `[2/10]`, etc. while processing
- **Multiple sort options** - Choose from Hot, Top, New, or Rising posts
- **Time filters for Top posts** - Select All time, Year, Month, Week, or Day
- **Post preview during processing** - Shows author, score, and text preview
- **Summary report** - Displays success rate and output directory path
- **Better prompts** - Clear instructions with examples and defaults

#### Features Added
- **Sort type selection** - Hot, Top (with time filters), New, Rising
- **Post metadata display** - Shows author, score, and text preview
- **Empty content handling** - Skips posts with no text
- **Success tracking** - Counts and reports successful conversions
- **Text content combination** - Improved concatenation with proper punctuation

#### Code Quality
- **PEP 8 compliant** - Proper naming conventions and formatting
- **Meaningful variable names** - `safe_title` instead of `ttsfeed`
- **Removed code smell** - Replaced 5 blank `print()` with `print('\n' * 5)` equivalent
- **Comments and documentation** - Clear inline comments explaining logic
- **Consistent string formatting** - Uses f-strings throughout

### 🐛 Bug Fixes
- Fixed broken filename generation that created `Submission(id='abc').mp3` files
- Fixed missing directory creation (files now save to `audio_output/`)
- Fixed language code (changed `'en-US'` to `'en'` - gTTS uses ISO 639-1)
- Fixed potential crashes from invalid user input

### 📁 New Files
- **requirements.txt** - Properly specifies dependencies (`praw>=7.7.0`, `gTTS>=2.3.0`)
- **.gitignore** - Ignores audio files, Python cache, virtual environments, and IDE files

### 🔧 Technical Details
- Line count: 67 → 287 lines (but with proper structure and documentation)
- Functions: 0 → 8 functions
- Error handlers: 0 → 6 try-except blocks
- Input validation: None → 4 validation checks

### ⚠️ Breaking Changes
- Output directory changed from current directory to `audio_output/` subfolder
- Filename format changed from `Submission(...).mp3` to `{id}_{title}.mp3`
- Interactive prompts now have more options (sort type, time filter)

### 📝 Notes
- Credentials remain unchanged as requested
- Balcon support remains commented out (external dependency)
- All original functionality preserved and enhanced
