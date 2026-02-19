# Coffee Meme Generator

A Python script that automatically generates coffee memes using AI and sends them to your email. Perfect for daily coffee humor!

## Features

- 🤖 **AI-Powered**: Generates meme captions and images using **OpenAI** (GPT + gpt-image-1 or DALL-E 3) or **Grok** (xAI)
- 🎨 **Two-Step Generation**: First generates funny text, then creates a coffee meme image that displays that exact text
- 📧 **Email Delivery**: Sends memes directly to your email (forward to group chats or use the iPhone automation below)
- ⏰ **Automated**: Can be scheduled to run daily using Windows Task Scheduler
- 🖼️ **Auto-Optimization**: Automatically resizes and compresses images for email compatibility

## Prerequisites

- Python 3.8 or higher
- **Either** an OpenAI API account and key **or** an xAI (Grok) API account and key
- Email account (Gmail, Outlook, or any SMTP-compatible email)
- (Optional) ImgBB / Imgur API keys for image hosting—not required for email delivery

## Setup Instructions

### 1. Clone or Download This Project

Make sure you have all the files in a directory on your computer.

### 2. Install Python Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

### 3. Get API Keys

Choose one AI provider (OpenAI or Grok). You only need the API key for the provider you use.

#### OpenAI API Key (when using OpenAI)

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key (you won't be able to see it again!)

#### Grok / xAI API Key (when using Grok)

1. Go to [xAI](https://x.ai/) and sign up or log in
2. Open the [xAI API Console](https://console.x.ai/)
3. Go to [API Keys](https://console.x.ai/team/default/api-keys)
4. Create a new API key and copy it
5. Ensure your account has credits (new users may receive free credits)

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
# AI Provider: "openai" or "grok" (default: openai)
AI_PROVIDER=openai

# OpenAI API (required when AI_PROVIDER=openai)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Grok / xAI API (required when AI_PROVIDER=grok)
XAI_API_KEY=your-xai-api-key-here

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=true
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password-here
RECIPIENT_EMAIL=recipient@example.com

# OpenAI image settings (when AI_PROVIDER=openai, optional)
TEXT_MODEL=gpt-4o-mini
OPENAI_MODEL=gpt-image-1
IMAGE_SIZE=1024x1024
IMAGE_QUALITY=low
MAX_IMAGE_SIZE_MB=5.0

# Grok image settings (when AI_PROVIDER=grok, optional)
GROK_TEXT_MODEL=grok-2-latest
GROK_IMAGE_MODEL=grok-imagine-image
GROK_ASPECT_RATIO=1:1
GROK_RESOLUTION=1k

# Meme Style (optional)
MEME_STYLE=funny

# Image Hosting (optional - not needed for email)
IMGBB_API_KEY=your_imgbb_api_key_here
IMGUR_CLIENT_ID=your_imgur_client_id_here
```

3. Replace all the placeholder values with your actual credentials:
   - `AI_PROVIDER`: Set to `openai` or `grok` (default: `openai`). **When OpenAI**: set `OPENAI_API_KEY`. **When Grok**: set `XAI_API_KEY`. Optional for Grok: `GROK_TEXT_MODEL`, `GROK_IMAGE_MODEL`, `GROK_ASPECT_RATIO`, `GROK_RESOLUTION`.
   - `SMTP_SERVER`: Your email provider's SMTP server (e.g., `smtp.gmail.com` for Gmail, `smtp-mail.outlook.com` for Outlook)
   - `SMTP_PORT`: SMTP port (usually `587` for TLS, `465` for SSL)
   - `SMTP_USE_TLS`: Set to `true` for TLS (port 587) or `false` for SSL (port 465)
   - `EMAIL_ADDRESS`: Your email address (the one sending the memes)
   - `EMAIL_PASSWORD`: Your email password or app password (see setup instructions above)
   - `RECIPIENT_EMAIL`: Recipient email address(es)—use comma-separated list for multiple recipients (e.g. your iPhone’s email for the automation below)
   - OpenAI-only (optional): `TEXT_MODEL`, `OPENAI_MODEL`, `IMAGE_SIZE`, `IMAGE_QUALITY`
   - `IMGBB_API_KEY` / `IMGUR_CLIENT_ID`: Optional; not needed for email

**Important**: 
- For Gmail, you must use an app password (not your regular password)
- For multiple recipients, separate email addresses with commas: `email1@example.com,email2@example.com`
- Keep your `.env` file secure and never commit it to version control

### 5. Test the Script

Run the script manually to make sure everything works:

```bash
python meme_generator.py
```

You should receive a coffee meme at the configured email address within a few minutes. To have it auto-sent to a group chat on your iPhone, see [iPhone: Auto-Send Meme Email Attachment to a Group Chat](#iphone-auto-send-meme-email-attachment-to-a-group-chat).

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
3. Check your email (and group chat if you use the iPhone automation below) for the meme
4. Check the log file `meme_generator.log` for any errors

## iPhone: Auto-Send Meme Email Attachment to a Group Chat

You can use an **iPhone Shortcuts automation** so that when you receive the coffee meme email, the image attachment is automatically sent to a group chat (e.g. iMessage or WhatsApp). This uses the built-in **Shortcuts** app and **Automation** (triggered by email).

### What you need

- iPhone with the **Mail** app and **Shortcuts** (built in)
- Your meme emails delivered to this iPhone (set `RECIPIENT_EMAIL` to your iPhone’s email, or forward to it)
- The group chat created in Messages (or another app) so you can select it in the shortcut

### Option A: Automation when an email is received

1. **Create the shortcut first** (so you can attach it to the automation):
   - Open **Shortcuts** → **Shortcuts** tab → **+** (New Shortcut).
   - Add action **“Find Emails”**:
     - Set **Account** to the mailbox that receives the meme emails.
     - Set **Sender** to your `EMAIL_ADDRESS` (the address that sends the memes), or leave blank to use “most recent” from that account.
     - Set **Limit** to **1** (only the latest matching email).
   - Add action **“Get contents of”** (or **“Get File from Input”** / **“Get Attachments from Input”** depending on your iOS version—use the action that gives you the attachment from the email).
   - If your version exposes **“Get attachments from Mail”** or **“Contents of Mail”** and then “Get first attachment”, use that to pass the image.
   - Add action **“Send Message”**:
     - **Recipients**: tap and choose your **group chat** (or contact).
     - Leave message body blank or add a short line (e.g. “☕”); the **input** from the previous step should be attached as the image. If the action has “Input” or “Attachments”, pass the attachment there.
   - Name the shortcut (e.g. **“Meme to group”**) and tap **Done**.

2. **Create the automation**:
   - In Shortcuts, open the **Automation** tab → **+** → **Create Personal Automation**.
   - Choose **Email**:
     - **Sender**: your `EMAIL_ADDRESS` (the meme sender).
     - Optionally **Subject Contains**: e.g. `Coffee` or `Meme` if your email subject is consistent.
     - **Account**: the mailbox where you receive the meme.
   - Tap **Next** → **Add Action** → search for **“Run Shortcut”** → select the shortcut you created (e.g. **“Meme to group”**).
   - Tap **Next** → turn **Ask Before Running** **off** if you want it to run without a prompt (otherwise you’ll tap “Run” when notified).
   - Tap **Done**.

After this, when a matching email arrives, the automation runs and the shortcut should get that email’s attachment and send it to the group. If your iOS version doesn’t pass the email automatically into “Find Emails”, the shortcut still runs and can find the latest email from that sender.

### Option B: Manual shortcut (no automation)

If automation is unreliable or you prefer to trigger it yourself:

1. In **Shortcuts**, create a new shortcut.
2. Add **Find Emails** (same sender/account as above, Limit 1).
3. Add the action that gets the **attachment** from that email (e.g. “Get contents of” / “Get File from Input” / attachment from Mail).
4. Add **Send Message** to your group chat and pass the attachment as input.
5. Run the shortcut manually after you receive the meme email (e.g. from the Shortcuts widget or by asking Siri).

### Notes

- **Action names** can differ by iOS version (e.g. “Get contents of” vs “Get File from Input”). If you don’t see “Get attachments from Mail”, try “Find Emails” → “Get contents of” and see if the result includes the image, or search in the actions list for “attachment” or “Mail”.
- **Ask Before Running**: With “Ask Before Running” on, you’ll get a notification when the email arrives; tap **Run** to send the attachment to the group.
- **Subject line**: In your script, the email subject is set by `email_service`. If you use “Subject Contains” in the trigger, use a phrase that appears in that subject.

## Configuration Options

### AI Provider

- `AI_PROVIDER`: `openai` (default) or `grok`. Use `grok` to generate memes with xAI's Grok models (caption + grok-imagine-image).

### OpenAI Image Settings (when AI_PROVIDER=openai)

- `OPENAI_MODEL`: `gpt-image-1` (default), `gpt-image-1-mini`, `dall-e-3`, or `dall-e-2`. For gpt-image-1, sizes can be `1024x1024`, `1536x1024`, `1024x1536`; for DALL-E 3, `1024x1024`, `1792x1024`, `1024x1792`.
- `IMAGE_SIZE`: Depends on model (see above). Default: `1024x1024`.
- `IMAGE_QUALITY`: For gpt-image-1: `high`, `medium`, `low`, or `auto`. For DALL-E 3: `standard` or `hd`. Default in config: `low`.

### Grok Settings (when AI_PROVIDER=grok)

- `GROK_TEXT_MODEL`: Chat model for meme caption (e.g. `grok-2-latest`, `grok-3-mini`). Default: `grok-2-latest`.
- `GROK_IMAGE_MODEL`: Image model (default: `grok-imagine-image`).
- `GROK_ASPECT_RATIO`: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `auto`, etc. Default: `1:1`.
- `GROK_RESOLUTION`: `1k` or `2k`. Default: `1k`.

### Other

- `MAX_IMAGE_SIZE_MB`: Maximum image size for email (default: `5.0` MB).

### Meme Style

- `MEME_STYLE`: Style of meme. Options: `funny`, `motivational`, `relatable` (default: `funny`)

## Troubleshooting

### Script Fails with "Missing required environment variables"

- Make sure you created a `.env` file in the project directory
- Check that all required variables are set (no empty values)
- Verify there are no extra spaces or quotes around values

### "OpenAI API error" or "Invalid API key" (AI_PROVIDER=openai)

- Verify your OpenAI API key is correct
- Check that you have credits in your OpenAI account
- Ensure your API key hasn't been revoked

### Grok / xAI errors (AI_PROVIDER=grok)

- Ensure `XAI_API_KEY` is set in `.env` and `AI_PROVIDER=grok`
- Create or check your key at [xAI API Keys](https://console.x.ai/team/default/api-keys)
- Confirm your xAI account has credits
- If the text model name fails, try `grok-2-latest` or `grok-3-mini` (see [xAI models](https://docs.x.ai/docs/models))

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

- **OpenAI API** (when AI_PROVIDER=openai): 
  - **Caption**: One short GPT call per meme (e.g. gpt-4o-mini), typically a fraction of a cent.
  - **Image**: gpt-image-1 or DALL-E 3; pricing varies by model and quality. DALL-E 3 is roughly ~$0.04 (standard) or ~$0.08 (HD) per image. Check [OpenAI pricing](https://developers.openai.com/api/docs/pricing/) for current rates.
  - Estimated daily cost: a few cents per meme depending on model and quality.
- **Grok / xAI** (when AI_PROVIDER=grok): 
  - **Caption**: One short Grok chat call per meme; pricing is token-based (see [xAI pricing](https://docs.x.ai/docs/models)).
  - **Image**: grok-imagine-image uses per-image pricing. See [xAI models and pricing](https://docs.x.ai/docs/models) for current rates. New xAI accounts may receive free credits.
- **Email**: 
  - **Free!** Most email providers (Gmail, Outlook, etc.) offer free SMTP sending—no per-message fees.

## License

This project is provided as-is for personal use.

## Support

For issues or questions:
1. Check the log file `meme_generator.log`
2. Verify all API keys and email configuration
3. Test each component individually (OpenAI or Grok, email settings)
4. Make sure you're using an app password for Gmail (not your regular password)

Enjoy your daily coffee memes! ☕
