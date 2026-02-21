# WhatsApp Chat Analyzer

## Overview
The **WhatsApp Chat Analyzer** is a Python-based tool that analyzes your exported WhatsApp chat history to provide insights into your messaging patterns. It can generate statistics, word clouds, emoji usage, and other metrics to help you understand your chat behavior.

## Features
- Analyzes individual or group chats.
- Provides statistics: total messages, words, media files, links, and emojis.
- Generates word clouds for frequently used words.
- Visualizes emoji usage and trends over time.
- Supports filtering by user or date range.
- Export analysis results to CSV or graphical format.

## Dataset
- The tool uses **exported WhatsApp chat text files (.txt)**.
- Chat files should be exported from WhatsApp without media for full text analysis.
- Example format:
```
[12/31/2025, 23:59] John Doe: Happy New Year!
[01/01/2026, 00:01] Jane Doe: Happy New Year to you too!
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/zk747933-jpg/Whattsapp-Chat-Analyzer
cd whatsapp-chat-analyzer
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. **Run the Analyzer**  
```bash
python analyze_chat.py --file path_to_chat.txt
```

2. **Optional Filters:**
```bash
python analyze_chat.py --file chat.txt --user "John Doe" --start-date 2026-01-01 --end-date 2026-02-01
```

3. **Example in Python:**
```python
from analyzer import WhatsAppChatAnalyzer

analyzer = WhatsAppChatAnalyzer('chat.txt')
stats = analyzer.get_statistics()
print(stats)

analyzer.generate_wordcloud(output_file='wordcloud.png')
analyzer.plot_emoji_usage()
```

## Requirements
- Python 3.8+
- pandas
- matplotlib
- wordcloud
- emoji
- urlextract

Install all requirements with:
```bash
pip install pandas matplotlib wordcloud emoji urlextract
```

## Project Structure
```
WhatsApp-Chat-Analyzer/
│
├── data/
│   └── chat.txt             # Example WhatsApp chat file
├── analyzer.py              # WhatsAppChatAnalyzer class
├── analyze_chat.py          # Script to run analysis
├── requirements.txt         # Required packages
└── README.md                # Project documentation
```

## Contributing
1. Fork the repository
2. Create your feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Add feature"`
4. Push to the branch: `git push origin feature-name`
5. Create a Pull Request

## License
This project is licensed under the **MIT License**.

