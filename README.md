# Telegram Avatar Changer

![Static Badge](https://img.shields.io/badge/python-3.12-blue)
![Static Badge](https://img.shields.io/badge/Telethon-1.36.0-blue)
![Static Badge](https://img.shields.io/badge/Pillow-10.4.0-seagreen)

This project is a Python script that uses the Telegram Core API to periodically change a user's avatar. It offers several operating modes for avatar selection and generation.

## Features

- Multiple avatar generation modes:
  - Select from default Reddit avatars
  - Construct unique characters from elements similar to Reddit
  - Obtain random avatars from a generator
  - Use random images from a Telegram channel
- Configurable update frequency
- Safe for Work (SFW) mode with customizable hours and days
- Easy start/stop control via Telegram messages

## Demo

You can see a demo of the script in action [here](https://youtu.be/6ZB7xAUKQv4).

## Prerequisites

- Python 3.7+
- Telegram API credentials (api_id and api_hash)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/naztar0/TelegramAvatarChanger.git
   cd TelegramAvatarChanger
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Copy `config.example.json` to `config.json` and fill in your Telegram API credentials and other settings.

## Configuration

Edit the `config.json` file to customize the behavior of the avatar changer:

- `api_id` and `api_hash`: Your Telegram API credentials
- `phone_number`: Your Telegram account phone number
- `2fa_password`: Your Two-Factor Authentication password (if enabled)
- `sleep_time`: Time between avatar changes (in seconds)
- `mode`: Avatar generation mode ("snoo_v1", "snoo_v2", "txdne", or "channel")
- `profile`: Your Telegram profile information
- `sfw_mode`: Settings for Safe for Work mode
- `channel`: Settings for fetching avatars from a Telegram channel
- `snoo`: Configuration for the Snoo avatar generator

## Usage

Run the script:

```
python app
```

The script will start changing your Telegram avatar periodically based on the configured settings.

To control the script:
- Send "stop" to yourself on Telegram to pause avatar changes
- Send "start" to resume avatar changes

## Avatar Generation Modes

### 1. Snoo V1 (`snoo_v1`)
Selects random pre-generated Reddit-style avatars from the `assets/snoo_v1` directory.

### 2. Snoo V2 (`snoo_v2`)
Generates unique avatars by combining various parts (e.g., head, body, accessories) from the `assets/snoo_v2` directory.

### 3. This X Does Not Exist (`txdne`)
Fetches random AI-generated avatars from various "This X Does Not Exist" websites.

### 4. Telegram Channel (`channel`)
Selects random images from a specified Telegram channel to use as avatars.

## Safe for Work (SFW) Mode

When enabled, SFW mode changes your profile information during specified hours and days of the week, typically to maintain a professional appearance during work hours.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is for educational purposes only. Use responsibly and in accordance with Telegram's terms of service.
