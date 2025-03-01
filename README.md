# PUCC Availability System - Blueprint Document

## 1. Introduction
### Project Name: PUCC Availability System

### Purpose
Provides a clear, real-time status indicator for the PUCC within the ED. It reduces manual communication by displaying whether PUCC is accepting clients.

### Intended Users
- ED streaming RN
- ED ops

### Core Functionalities
- Full-Screen Touch UI displaying PUCC status
- Green (Available) / Red (Unavailable) indicators
- Manual Toggle with reason selection (large button interface)
- Automatic 'Unavailable' switch at 21:00 (configurable)
- Countdown timer when PUCC is unavailable (updates every minute)
- Comprehensive logging of all status changes, including reasons
- Stable, minimal scheduled tasks for lightweight operation
- Auto-reset after 60 minutes when PUCC is unavailable
- Automatic startup on boot
