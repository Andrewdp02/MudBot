# Coffee Meme Generator

A Python script that automatically generates coffee memes using AI and sends them to your email. Perfect for daily coffee humor!

## Features

- 🤖 **AI-Powered**: Uses OpenAI's DALL-E 3 to generate coffee meme images with captions
- 🎨 **Image Generation**: Creates coffee-themed meme images with text in one step
- 📧 **Email Delivery**: Sends memes directly to your email (can forward to group chats!)
- ⏰ **Automated**: Can be scheduled to run daily using Windows Task Scheduler
- 🖼️ **Auto-Optimization**: Automatically resizes and compresses images for email compatibility

## Prerequisites

- Python 3.8 or higher
- OpenAI API account and key
- Email account (Gmail, Outlook, or any SMTP-compatible email)
- (Optional) ImgBB API key - no longer required for email, but kept for potential future use

## Setup Instructions

### 1. Clone or Download This Project

Make sure you have all the files in a directory on your computer.

### 2. Install Python Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

### 3. Get API Keys

#### OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key (you won't be able to see it again!)

#### Email Account Setup

The script sends memes via email, which you can then forward to group chats or access on any device.

**For Gmail:**
1. Go to your [Google Account Settings](https://myaccount.google.com/)
2. Enable 2-Step Verification (required for app passwords)
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Create a new app password:
   - Select "Mail" and "Other (Custom name)"
   - Enter "Coffee Meme Generator" as the name
   - Click "Generate"
   - Copy the 16-character password (you'll use this in `.env`)

**For Outlook/Hotmail:**
1. Go to [Microsoft Account Security](https://account.microsoft.com/security)
2. Enable 2-Step Verification if not already enabled
3. Go to [App Passwords](https://account.microsoft.com/security/app-passwords)
4. Create a new app password for "Mail"
5. Copy the password

**For Other Email Providers:**
- Check your email provider's documentation for SMTP settings
- You may need to enable "Less secure app access" or create an app-specific password
- Common SMTP settings:
  - **Gmail**: smtp.gmail.com, port 587 (TLS)
  - **Outlook**: smtp-mail.outlook.com, port 587 (TLS)
  - **Yahoo**: smtp.mail.yahoo.com, port 587 (TLS)
  - **Custom**: Check with your email provider

### 4. Configure Environment Variables

1. Create a file named `.env` in the project directory
2. Copy the contents from `.env.example` (if it exists) or use this template:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=true
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password-here
RECIPIENT_EMAIL=recipient@example.com

# Image Generation Settings (optional)
IMAGE_SIZE=1024x1024
IMAGE_QUALITY=low
MAX_IMAGE_SIZE_MB=5.0

# Meme Style (optional)
MEME_STYLE=funny

# Image Hosting (optional - not needed for email, but kept for potential future use)
IMGBB_API_KEY=your_imgbb_api_key_here
IMGUR_CLIENT_ID=your_imgur_client_id_here
```

3. Replace all the placeholder values with your actual credentials:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `SMTP_SERVER`: Your email provider's SMTP server (e.g., `smtp.gmail.com` for Gmail, `smtp-mail.outlook.com` for Outlook)
   - `SMTP_PORT`: SMTP port (usually `587` for TLS, `465` for SSL)
   - `SMTP_USE_TLS`: Set to `true` for TLS (port 587) or `false` for SSL (port 465)
   - `EMAIL_ADDRESS`: Your email address (the one sending the memes)
   - `EMAIL_PASSWORD`: Your email password or app password (see setup instructions above)
   - `RECIPIENT_EMAIL`: Recipient email address(es) - use comma-separated list for multiple recipients
   - `IMGBB_API_KEY`: (Optional) Not needed for email, but kept for potential future use
   - `IMGUR_CLIENT_ID`: (Optional) Not needed for email, but kept for potential future use

**Important**: 
- For Gmail, you must use an app password (not your regular password)
- For multiple recipients, separate email addresses with commas: `email1@example.com,email2@example.com`
- Keep your `.env` file secure and never commit it to version control

### 5. Test the Script

Run the script manually to make sure everything works:

```bash
python meme_generator.py
```

You should receive a coffee meme on your phone within a few minutes!

## Setting Up Windows Task Scheduler

To run the script automatically every day:

### Method 1: Using Task Scheduler GUI

1. Open **Task Scheduler**:
   - Press `Win + R`, type `taskschd.msc`, and press Enter
   - Or search for "Task Scheduler" in the Start menu

2. Create a new task:
   - Click "Create Basic Task" in the right panel
   - Name: "Daily Coffee Meme"
   - Description: "Generate and send daily coffee meme"
   - Click "Next"

3. Set trigger:
   - Trigger: "Daily"
   - Start date: Today's date
   - Start time: Choose when you want to receive memes (e.g., 8:00 AM)
   - Click "Next"

4. Set action:
   - Action: "Start a program"
   - Program/script: Full path to Python executable
     - Example: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe`
     - To find your Python path, run: `where python` in Command Prompt
   - Add arguments: `meme_generator.py`
   - Start in: Full path to your project directory
     - Example: `C:\Users\adell\Software Projects\MudBot`
   - Click "Next"

5. Review and finish:
   - Review your settings
   - Check "Open the Properties dialog for this task when I click Finish"
   - Click "Finish"

6. Configure additional settings (in Properties):
   - **General tab**:
     - Check "Run whether user is logged on or not" (if you want it to run when you're away)
     - Check "Run with highest privileges" (if needed)
   - **Conditions tab**:
     - Uncheck "Start the task only if the computer is on AC power" (if you want it on battery too)
   - **Settings tab**:
     - Check "Allow task to be run on demand"
     - Check "If the task fails, restart every:" and set to 1 hour (optional, for retries)
   - Click "OK"

### Method 2: Using Command Line (PowerShell as Administrator)

```powershell
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "meme_generator.py" -WorkingDirectory "C:\Users\adell\Software Projects\MudBot"
$trigger = New-ScheduledTaskTrigger -Daily -At "8:00AM"
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive
Register-ScheduledTask -TaskName "Daily Coffee Meme" -Action $action -Trigger $trigger -Principal $principal -Description "Generate and send daily coffee meme"
```

**Note**: Replace the paths and time with your actual values.

### Testing the Scheduled Task

1. In Task Scheduler, find your task
2. Right-click and select "Run"
3. Check your phone for the meme
4. Check the log file `meme_generator.log` for any errors

## Configuration Options

### Image Settings

- `IMAGE_SIZE`: Image dimensions. Options: `1024x1024`, `1792x1024`, `1024x1792` (default: `1024x1024`)
- `IMAGE_QUALITY`: Image quality. Options: `standard` or `hd` (default: `standard`)
- `MAX_IMAGE_SIZE_MB`: Maximum image size for email (default: `5.0` MB, most email providers support up to 25MB)

### Meme Style

- `MEME_STYLE`: Style of meme. Options: `funny`, `motivational`, `relatable` (default: `funny`)

## Troubleshooting

### Script Fails with "Missing required environment variables"

- Make sure you created a `.env` file in the project directory
- Check that all required variables are set (no empty values)
- Verify there are no extra spaces or quotes around values

### "OpenAI API error" or "Invalid API key"

- Verify your OpenAI API key is correct
- Check that you have credits in your OpenAI account
- Ensure your API key hasn't been revoked

### "Email error" or "Email not received"

- **SMTP Authentication Failed**: 
  - For Gmail: Make sure you're using an app password, not your regular password
  - Verify your email address and password are correct
  - Check that 2-Step Verification is enabled (required for app passwords)
- **Connection Errors**:
  - Verify your SMTP server and port are correct
  - Check your firewall/antivirus isn't blocking the connection
  - Try different ports: 587 (TLS) or 465 (SSL)
- **Email Not Received**:
  - Check your spam/junk folder
  - Verify the recipient email address is correct
  - Check that your email provider isn't blocking the message
  - For Gmail, check if "Less secure app access" needs to be enabled (older accounts)

### "Image upload failed" or hosting service errors

- **Note**: Image hosting is no longer required for email delivery. Images are sent as email attachments.
- If you see image hosting errors, they can be ignored (the image will still be sent via email)
- Image hosting code is kept for potential future use but is not actively used

### Task Scheduler doesn't run the script

- Check that Python path is correct in the task action
- Verify the "Start in" directory is correct
- Check Task Scheduler history for error messages
- Try running the script manually first to ensure it works
- Check the log file `meme_generator.log` for errors

### Image is too large for email

- Most email providers support attachments up to 25MB
- The script automatically compresses images, but very large images may still cause issues
- Try reducing `MAX_IMAGE_SIZE_MB` in your `.env` file if needed
- Default limit is 5MB which should work with all email providers

## Logs

The script creates a log file `meme_generator.log` in the project directory. Check this file for detailed information about script execution and any errors.

## Cost Considerations

- **OpenAI API**: 
  - DALL-E 3: ~$0.04 per image (standard), ~$0.08 per image (HD)
  - Estimated daily cost: ~$0.04-0.08 per meme (no GPT call needed since caption is generated with image)
- **Email**: 
  - **Free!** Most email providers (Gmail, Outlook, etc.) offer free SMTP sending
  - No API costs or per-message fees
  - Perfect for daily automated memes

## License

This project is provided as-is for personal use.

## Support

For issues or questions:
1. Check the log file `meme_generator.log`
2. Verify all API keys and email configuration
3. Test each component individually (OpenAI, email settings)
4. Make sure you're using an app password for Gmail (not your regular password)

Enjoy your daily coffee memes! ☕
