

# Database Schema and Spreadsheet Structure

This document defines the structure of the spreadsheet database that will be used to store the information gathered from the web crawling and research process. The goal is to create a highly detailed and organized dataset that can be used to train AI coding agents.

## Spreadsheet Structure

The spreadsheet will have the following columns:

| Field Name                | Data Type | Description                                                                                                                                 | Example                                                                                                   |
| ------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Category**              | String    | The main category of the information (e.g., Features, Architecture, UI/UX, Use Cases, Integrations, Design, Workflows, Templates, Guidelines). | `Features`                                                                                                |
| **Sub-category**          | String    | A more specific sub-category that provides further classification within the main category.                                                 | `Core Features`                                                                                           |
| **Title**                 | String    | A concise and descriptive title for the information being documented.                                                                       | `User Authentication`                                                                                     |
| **Topic**                 | String    | The specific topic or aspect being addressed within the title.                                                                              | `Two-Factor Authentication`                                                                               |
| **Detail**                | Text      | A comprehensive description of the information, including its purpose, functionality, technical details, and how it works.                  | `Users can enable 2FA using an authenticator app. The system generates a QR code for setup...`              |
| **Specific URL**          | URL       | The exact URL where the information was found. This serves as a direct reference and citation.                                              | `https://example.com/docs/security/2fa`                                                                   |
| **Identify Tags**         | String    | Comma-separated keywords or tags that describe the information, facilitating search and filtering.                                          | `#security, #authentication, #2FA`                                                                        |
| **Summary**               | Text      | A brief summary of the detailed information, providing a quick overview.                                                                    | `The application supports two-factor authentication (2FA) via authenticator apps to enhance user security.` |
| **Raw Data**              | Text      | The raw, unformatted text or HTML content from which the information was extracted. This is crucial for context and further analysis.       | `(Raw HTML snippet of the 2FA documentation page)`                                                        |

