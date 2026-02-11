@echo off
echo ========================================
echo Healthcare AI/ML Dashboard Deployment
echo ========================================
echo.

echo Step 1: Initializing Git repository...
git init
echo.

echo Step 2: Adding files to Git...
git add .
echo.

echo Step 3: Creating initial commit...
git commit -m "Healthcare AI/ML Dashboard - Initial Commit"
echo.

echo ========================================
echo Git repository initialized successfully!
echo ========================================
echo.

echo Next Steps:
echo 1. Create a new repository on GitHub: https://github.com/new
echo 2. Name it: healthcare-ai-ml-dashboard
echo 3. Run these commands (replace YOUR_USERNAME):
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/healthcare-ai-ml-dashboard.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. Then go to Vercel: https://vercel.com
echo 5. Import your GitHub repository
echo 6. Deploy!
echo.

pause
