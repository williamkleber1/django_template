# Model Documentation

This document provides detailed information about all the models used in the Django Template API.

## Access Models

### CustomUserModel

The main user model that extends Django's AbstractUser with additional functionality for the application.

**Table Name:** `access_customusermodel`

**Key Features:**
- Email-based authentication (instead of username)
- Integration with Stripe for payments
- Credit system for feature usage
- Avatar/profile picture support
- Email confirmation workflow
- Device tracking
- Notification preferences

**Fields:**

| Field | Type | Description | Required | Default |
|-------|------|-------------|----------|---------|
| `userId` | CharField(64) | Primary key, auto-generated UUID | Yes | `uuid4()` |
| `username` | CharField(100) | Optional username, can be null | No | `null` |
| `email` | EmailField(100) | Unique email address for authentication | Yes | - |
| `avatar` | ImageField | Profile picture stored in private media | No | `null` |
| `stripeCustomerId` | CharField(100) | Stripe customer ID for payment integration | No | `null` |
| `dalle_credits` | IntegerField | Credits for DALL-E image generation | Yes | `0` |
| `subscription_credits` | IntegerField | Credits from subscription plans | Yes | `0` |
| `domainShopperId` | CharField(100) | Domain shopping service integration ID | No | `null` |
| `is_deactivated` | BooleanField | Whether the account is deactivated | Yes | `False` |
| `is_complimentary_plan` | BooleanField | Whether user has a free/complimentary plan | Yes | `False` |
| `phone_number` | CharField(15) | Phone number in E.164 format | No | `null` |
| `birth_date` | DateField | User's birth date | No | `null` |
| `is_email_confirmed` | BooleanField | Whether email has been confirmed | Yes | `False` |
| `notification_settings` | JSONField | User notification preferences | No | `default_notification_settings()` |
| `created` | DateTimeField | Account creation timestamp | Yes | `auto_now_add` |
| `updated` | DateTimeField | Last update timestamp | Yes | `auto_now` |

**Methods:**
- `whoami`: Property that returns a dictionary with basic user info (email, username, avatar, credits)

**Authentication:**
- Uses email as the primary authentication field
- Integrates with JWT tokens for API authentication
- Custom user manager handles user creation

### ResetPasswordControl

Tracks password reset requests for security and audit purposes.

**Table Name:** `access_resetpasswordcontrol`

**Fields:**

| Field | Type | Description | Required | Default |
|-------|------|-------------|----------|---------|
| `request_id` | CharField(64) | Primary key, auto-generated UUID | Yes | `uuid4()` |
| `email` | EmailField(200) | Email address requesting password reset | Yes | - |
| `date` | DateTimeField | When the reset request was created | Yes | `auto_now_add` |

**Usage:** 
Used to track password reset requests and prevent abuse by limiting the frequency of requests per email.

### PasswordRecoveryEmail

Email templates for password recovery communications.

**Table Name:** `access_passwordrecoveryemail`

**Fields:**

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `id` | AutoField | Primary key | Yes |
| `name` | CharField(100) | Template name/identifier | Yes |
| `body` | TextField | Email body content | Yes |
| `subject` | CharField(200) | Email subject line | Yes |
| `email_address` | EmailField(200) | Recipient email address | Yes |

**Usage:**
Stores customizable email templates for password recovery workflows, allowing for personalized communication.

### EmailConfirmationControl

Manages email confirmation requests for user verification.

**Table Name:** `access_emailconfirmationcontrol`

**Fields:**

| Field | Type | Description | Required | Default |
|-------|------|-------------|----------|---------|
| `id` | AutoField | Primary key | Yes | - |
| `email` | EmailField | Email address to be confirmed | Yes | - |
| `date` | DateTimeField | When confirmation was requested | Yes | `auto_now_add` |

**Usage:**
Tracks email confirmation requests and helps manage the email verification workflow.

### PreRegister

Collects email addresses for pre-registration and waitlist functionality.

**Table Name:** `access_preregister`

**Inheritance:** Extends `BaseModel` (from `general.abstract_models`)

**Fields:**

| Field | Type | Description | Required | Default |
|-------|------|-------------|----------|---------|
| `id` | CharField(64) | Primary key UUID (from BaseModel) | Yes | `uuid4()` |
| `email` | EmailField(200) | Email address for pre-registration | Yes | - |
| `date` | DateTimeField | Registration timestamp | Yes | `auto_now_add` |
| `created` | DateTimeField | Created timestamp (from BaseModel) | Yes | `auto_now_add` |
| `updated` | DateTimeField | Updated timestamp (from BaseModel) | Yes | `auto_now` |

**Usage:**
Allows collection of interested user emails before full registration is available, useful for waitlists and early access programs.

### LoggedDevice

Tracks devices that users have logged in from for security monitoring.

**Table Name:** `access_loggeddevice`

**Inheritance:** Extends `BaseModel` (from `general.abstract_models`)

**Fields:**

| Field | Type | Description | Required | Default |
|-------|------|-------------|----------|---------|
| `id` | CharField(64) | Primary key UUID (from BaseModel) | Yes | `uuid4()` |
| `user` | ForeignKey | Reference to CustomUserModel | No | `null` |
| `device_type` | CharField(10) | Type: 'desktop' or 'mobile' | No | `null` |
| `device_name` | CharField(255) | Device identifier (e.g., browser name) | No | `null` |
| `last_login_at` | DateTimeField | Last login timestamp for this device | No | `timezone.now()` |
| `place` | CharField(100) | Location/place of login | No | `'unknown'` |
| `created` | DateTimeField | Created timestamp (from BaseModel) | Yes | `auto_now_add` |
| `updated` | DateTimeField | Updated timestamp (from BaseModel) | Yes | `auto_now` |

**Constraints:**
- Unique together: (`user`, `device_type`, `device_name`)

**Methods:**
- `update_last_login()`: Updates the last_login_at field to current time

**Usage:**
Provides security monitoring by tracking devices users log in from, helping detect unauthorized access.

## General Models

### BaseModel (Abstract)

Base abstract model that provides common fields for other models.

**Fields:**

| Field | Type | Description | Required | Default |
|-------|------|-------------|----------|---------|
| `id` | CharField(64) | Primary key UUID | Yes | `uuid4()` |
| `created` | DateTimeField | Creation timestamp | Yes | `auto_now_add` |
| `updated` | DateTimeField | Last update timestamp | Yes | `auto_now` |

**Usage:**
Extended by other models to provide consistent ID and timestamp fields across the application.

## Relationships

### User Relationships
- **CustomUserModel** → **LoggedDevice**: One-to-many (user can have multiple devices)
- **CustomUserModel**: Integrates with Django's built-in User groups and permissions

### Email Management Relationships
- **ResetPasswordControl**: Standalone model, linked to users via email field
- **EmailConfirmationControl**: Standalone model, linked to users via email field
- **PasswordRecoveryEmail**: Standalone email template model

### Registration Flow
- **PreRegister** → **CustomUserModel**: Pre-registration emails can later be converted to full user accounts

## Security Considerations

1. **Password Storage**: All passwords are hashed using Django's built-in password hashers
2. **Email Verification**: Users must confirm their email addresses before full account activation
3. **Device Tracking**: Login attempts are tracked by device for security monitoring
4. **UUID Primary Keys**: All models use UUIDs instead of sequential integers to prevent enumeration attacks
5. **Reset Request Tracking**: Password reset requests are logged to prevent abuse

## Integration Points

1. **Stripe Integration**: CustomUserModel includes `stripeCustomerId` for payment processing
2. **File Storage**: Avatar images use custom private media storage backend
3. **JWT Authentication**: CustomUserModel integrates with Simple JWT for token-based authentication
4. **Celery Tasks**: User-related background tasks can reference users via their UUID
5. **Monitoring**: Models include timestamps for audit trails and monitoring

## Default Settings

### Notification Settings Structure
```json
{
  "email": {
    "updates": false,
    "tips": false, 
    "payment": false
  },
  "push": {
    "updates": false,
    "tips": false,
    "payment": false
  }
}
```

This structure allows users to control different types of notifications across multiple channels.