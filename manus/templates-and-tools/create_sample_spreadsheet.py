#!/usr/bin/env python3
"""
Create a sample spreadsheet with example data for the web crawling and research database.
"""

import pandas as pd
from datetime import datetime

# Sample data for the spreadsheet
sample_data = [
    {
        'Category': 'Features',
        'Sub-category': 'Core Features',
        'Title': 'User Authentication',
        'Topic': 'Two-Factor Authentication',
        'Detail': 'Users can enable 2FA using an authenticator app. The system generates a QR code for setup and requires a 6-digit code for login. Supports TOTP (Time-based One-Time Password) algorithm compatible with Google Authenticator, Authy, and other standard authenticator apps.',
        'Specific URL': 'https://example.com/docs/security/2fa',
        'Identify Tags': '#security, #authentication, #2FA, #TOTP',
        'Summary': 'The application supports two-factor authentication (2FA) via authenticator apps to enhance user security.',
        'Raw Data': '<div class="security-section"><h2>Two-Factor Authentication</h2><p>Enable 2FA for enhanced security...</p></div>'
    },
    {
        'Category': 'Architecture',
        'Sub-category': 'Backend Systems',
        'Title': 'API Gateway',
        'Topic': 'Rate Limiting',
        'Detail': 'The API Gateway implements rate limiting to prevent abuse and ensure fair usage. Default limits are 1000 requests per hour for authenticated users and 100 requests per hour for unauthenticated users. Rate limits can be customized per user tier (Basic, Pro, Enterprise).',
        'Specific URL': 'https://example.com/docs/api/rate-limiting',
        'Identify Tags': '#API, #rate-limiting, #gateway, #backend',
        'Summary': 'API Gateway enforces rate limiting with tiered access controls based on user authentication and subscription level.',
        'Raw Data': '<section id="rate-limiting"><h3>Rate Limiting</h3><table><tr><th>User Type</th><th>Requests/Hour</th></tr>...</table></section>'
    },
    {
        'Category': 'UI/UX',
        'Sub-category': 'Design System',
        'Title': 'Color Palette',
        'Topic': 'Primary Colors',
        'Detail': 'The primary color palette consists of: Brand Blue (#2563EB), Success Green (#10B981), Warning Orange (#F59E0B), Error Red (#EF4444), and Neutral Gray (#6B7280). All colors meet WCAG 2.1 AA accessibility standards for contrast ratios.',
        'Specific URL': 'https://example.com/design-system/colors',
        'Identify Tags': '#design-system, #colors, #accessibility, #WCAG',
        'Summary': 'Standardized color palette with accessibility-compliant contrast ratios for consistent UI design.',
        'Raw Data': '<div class="color-palette"><div class="color-swatch" data-color="#2563EB">Brand Blue</div>...</div>'
    },
    {
        'Category': 'Use Cases',
        'Sub-category': 'Business Workflows',
        'Title': 'Customer Onboarding',
        'Topic': 'Account Setup Process',
        'Detail': 'New customers complete a 4-step onboarding process: 1) Email verification, 2) Profile creation with company details, 3) Payment method setup, 4) Initial configuration wizard. The process includes progress indicators and can be saved and resumed at any step.',
        'Specific URL': 'https://example.com/help/onboarding',
        'Identify Tags': '#onboarding, #workflow, #customer-journey, #setup',
        'Summary': 'Structured 4-step onboarding process with progress tracking and resume capability.',
        'Raw Data': '<div class="onboarding-flow"><ol><li>Email Verification</li><li>Profile Creation</li>...</ol></div>'
    },
    {
        'Category': 'Integrations',
        'Sub-category': 'Third-party APIs',
        'Title': 'Payment Processing',
        'Topic': 'Stripe Integration',
        'Detail': 'Payment processing is handled through Stripe API v2023-10-16. Supports credit cards, ACH transfers, and digital wallets (Apple Pay, Google Pay). Webhook endpoints handle payment confirmations, failures, and subscription updates. PCI DSS compliant with tokenized card storage.',
        'Specific URL': 'https://example.com/docs/integrations/stripe',
        'Identify Tags': '#payments, #stripe, #PCI-DSS, #webhooks',
        'Summary': 'Stripe-powered payment processing with multiple payment methods and PCI compliance.',
        'Raw Data': '<code>stripe.paymentIntents.create({ amount: 2000, currency: "usd" })</code>'
    },
    {
        'Category': 'Workflows',
        'Sub-category': 'Automation',
        'Title': 'Email Campaigns',
        'Topic': 'Automated Drip Campaigns',
        'Detail': 'Users can create automated email sequences triggered by user actions or time delays. Campaign builder includes drag-and-drop interface, A/B testing capabilities, and detailed analytics. Supports personalization tokens, conditional logic, and integration with CRM systems.',
        'Specific URL': 'https://example.com/features/email-automation',
        'Identify Tags': '#email-marketing, #automation, #campaigns, #analytics',
        'Summary': 'Visual campaign builder for automated email sequences with A/B testing and analytics.',
        'Raw Data': '<div class="campaign-builder"><div class="trigger-node">User Signs Up</div><div class="delay-node">Wait 1 day</div>...</div>'
    },
    {
        'Category': 'Templates',
        'Sub-category': 'Email Templates',
        'Title': 'Welcome Email',
        'Topic': 'New User Template',
        'Detail': 'Pre-designed welcome email template with company branding, personalization fields for user name and company, getting started checklist, and links to key resources. Template is responsive and tested across major email clients (Gmail, Outlook, Apple Mail).',
        'Specific URL': 'https://example.com/templates/welcome-email',
        'Identify Tags': '#templates, #email, #welcome, #responsive',
        'Summary': 'Responsive welcome email template with personalization and cross-client compatibility.',
        'Raw Data': '<table class="email-template"><tr><td>Welcome {{user.name}} to {{company.name}}!</td></tr>...</table>'
    },
    {
        'Category': 'Guidelines',
        'Sub-category': 'Development Standards',
        'Title': 'Code Review Process',
        'Topic': 'Pull Request Guidelines',
        'Detail': 'All code changes require peer review through pull requests. PRs must include: descriptive title and description, linked issue number, test coverage for new features, documentation updates, and approval from at least one senior developer. Automated checks include linting, testing, and security scanning.',
        'Specific URL': 'https://example.com/docs/development/code-review',
        'Identify Tags': '#development, #code-review, #pull-requests, #quality',
        'Summary': 'Structured code review process with automated checks and peer approval requirements.',
        'Raw Data': '## Pull Request Checklist\n- [ ] Descriptive title\n- [ ] Linked issue\n- [ ] Tests included\n...'
    }
]

# Create DataFrame
df = pd.DataFrame(sample_data)

# Create Excel file with formatting
with pd.ExcelWriter('sample_crawl_database.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Crawl Data', index=False)
    
    # Get the workbook and worksheet
    workbook = writer.book
    worksheet = writer.sheets['Crawl Data']
    
    # Auto-adjust column widths
    for column in worksheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
        worksheet.column_dimensions[column_letter].width = adjusted_width

print(f"Sample spreadsheet created: sample_crawl_database.xlsx")
print(f"Number of sample records: {len(sample_data)}")
print(f"Columns: {', '.join(df.columns)}")
