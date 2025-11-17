# fal-aura-sr

AI-powered image enhancement using advanced super-resolution technology to transform low-quality images into crystal-clear, high-resolution results.

[中文文档](./README_zh-CN.md)

## Overview

fal-aura-sr is an OOMOL package that provides intelligent image enhancement capabilities powered by the fal-aura-sr AI service. Whether you have blurry photos, low-resolution images, or just want to improve visual quality, this package offers an easy-to-use solution for enhancing image clarity and detail.

The package works seamlessly with both remote images (via URL) and local files, automatically handling the upload, processing, and download workflow.

## Key Features

- **AI-Powered Enhancement**: Utilizes advanced super-resolution algorithms to improve image quality
- **Flexible Input**: Works with both remote image URLs and local files
- **Automatic Processing**: Built-in polling mechanism automatically waits for processing to complete
- **Cloud Integration**: Seamlessly uploads local files and downloads enhanced results
- **Easy to Use**: Simple drag-and-drop workflows for quick image enhancement
- **Batch Processing**: Process multiple images using reusable workflows

## Available Components

### Task Blocks

#### 1. Enhance Image Clarity
**Purpose**: Submit an image for AI enhancement

This block takes an image URL and submits it to the enhancement service. It returns a session ID that you can use to track the processing status.

**What it does**:
- Accepts a publicly accessible image URL
- Sends the image to the AI enhancement service
- Returns a session ID for tracking the enhancement progress

**When to use**: When you want fine-grained control over the enhancement process or need to integrate with custom workflows.

---

#### 2. Query Conversion Result
**Purpose**: Check enhancement status and retrieve results

This block checks the processing status of your enhancement task and retrieves the enhanced image URL when ready. It includes smart polling functionality that automatically waits for completion.

**What it does**:
- Queries the status of an enhancement task using the session ID
- Automatically polls until the task completes (configurable)
- Returns the enhanced image URL when processing is finished

**When to use**: After submitting an image for enhancement, use this to get the final result.

---

### Subflows (Ready-to-Use Workflows)

#### 1. URL Image Enhancement
**Purpose**: Enhance images from remote URLs in one step

This is a complete, ready-to-use workflow that handles the entire enhancement process for remote images.

**What it does**:
1. Takes an image URL as input
2. Submits it for AI enhancement
3. Automatically waits for processing to complete
4. Returns the URL of the enhanced image

**Perfect for**:
- Enhancing images hosted on websites
- Processing images from cloud storage
- Working with social media images
- Any scenario where you already have an image URL

**Example use case**: You have a collection of product photos on your website that are low quality. Simply provide the URLs, and this workflow will enhance them automatically.

---

#### 2. Local Image Enhancement
**Purpose**: Enhance images from your computer in one step

This is a complete, ready-to-use workflow that handles everything from upload to download for local images.

**What it does**:
1. Takes a local image file as input
2. Uploads it to cloud storage
3. Submits it for AI enhancement
4. Automatically waits for processing to complete
5. Downloads the enhanced result to your specified location

**Perfect for**:
- Enhancing photos from your camera or phone
- Batch processing local image collections
- Improving scanned documents or old photos
- Any scenario where you have images on your local machine

**Example use case**: You have a folder of old family photos that are blurry or faded. Select each image, choose where to save the enhanced version, and this workflow handles the rest automatically.

---

## How to Use

### Using Subflows (Recommended for Most Users)

Subflows are pre-built, complete workflows that handle everything for you. Just provide the input and get the enhanced result.

#### For Remote Images (URL):
1. Open the **"URL Image Enhancement"** subflow
2. Provide the image URL
3. Run the workflow
4. Receive the enhanced image URL

#### For Local Files:
1. Open the **"Local Image Enhancement"** subflow
2. Select your local image file
3. Choose where to save the enhanced result (optional)
4. Run the workflow
5. Find your enhanced image at the saved location

### Using Task Blocks (For Advanced Users)

If you need to customize the workflow or integrate with other processes, you can use the individual task blocks:

1. Use **"Enhance Image Clarity"** to submit an image
2. Use **"Query Conversion Result"** to check status and retrieve results
3. Connect them together or integrate with other blocks as needed

## Technical Details

### API Integration
- **Endpoint**: `https://fusion-api.oomol.com/v1/fal-aura-sr/`
- **Authentication**: Automatically handled via OOMOL token
- **Processing**: Asynchronous with polling support

### Polling Configuration
The query block includes configurable polling options:
- **Enable Polling**: Automatically wait for completion (default: enabled)
- **Max Attempts**: Maximum number of status checks (default: 60)
- **Interval**: Time between checks in seconds (default: 5 seconds)

### Dependencies
This package relies on:
- **upload-to-cloud** (v0.0.5): For uploading local files to cloud storage
- **downloader** (v0.1.1): For downloading enhanced images

## Installation

This package is installed through the OOMOL platform. No manual installation is required.

### Dependencies
All required dependencies are automatically installed when you bootstrap the project:
```bash
npm install
poetry install --no-root
```

## Project Structure

```
fal-aura-sr/
├── tasks/
│   ├── enhance-image-clarity/      # Submit images for enhancement
│   └── query-conversion-result/    # Query and retrieve results
├── subflows/
│   ├── enhance-url-image/          # Complete workflow for remote images
│   └── enhance-local-image/        # Complete workflow for local files
├── flows/
│   └── flow-1/                     # Example/test workflows
├── package.oo.yaml                 # Package configuration
├── pyproject.toml                  # Python dependencies
├── package.json                    # Node.js dependencies
└── README.md                       # This file
```

## Support and Feedback

For issues, questions, or feedback about this package, please contact the OOMOL support team or refer to the OOMOL documentation.

## Version

Current version: 0.0.1

---

**Built with OOMOL** - The visual programming platform for AI workflows
