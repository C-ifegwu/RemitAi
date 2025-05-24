/**
 * RemitAI UI Component Design System
 * 
 * This file documents the component architecture and design decisions
 * for the RemitAI frontend, inspired by the provided design reference.
 */

/**
 * DESIGN PRINCIPLES
 * -----------------
 * 1. Clean, minimal aesthetic with ample white space
 * 2. Strong visual hierarchy with clear typography
 * 3. Vibrant but selective use of color (primarily yellow and green accents)
 * 4. Rounded corners and soft shadows for a friendly, approachable feel
 * 5. Consistent spacing and alignment throughout the interface
 * 6. Subtle animations and transitions for a polished experience
 */

/**
 * COLOR PALETTE
 * -------------
 * Primary (Yellow): #ffd60a - Used for CTAs, highlights, and key UI elements
 * Secondary (Green): #34bd6c - Used for success states, confirmations, and secondary actions
 * Neutrals: Various grays from #f8f9fa to #212529 - Used for text, backgrounds, and borders
 * 
 * Additional accent colors used sparingly:
 * - Error/Danger: #e03131
 * - Warning: #f08c00
 * - Info: #1971c2
 */

/**
 * TYPOGRAPHY
 * ----------
 * Headings: Poppins (font-display) - Bold, clean, modern
 * Body: Inter (font-sans) - Highly readable, versatile
 * 
 * Type Scale:
 * - Display/Hero: 3rem (48px)
 * - H1: 2.25rem (36px)
 * - H2: 1.875rem (30px)
 * - H3: 1.5rem (24px)
 * - H4: 1.25rem (20px)
 * - Body: 1rem (16px)
 * - Small: 0.875rem (14px)
 * - Caption: 0.75rem (12px)
 */

/**
 * COMPONENT ARCHITECTURE
 * ---------------------
 * The UI is built using a modular component architecture:
 * 
 * 1. Atoms - Basic building blocks
 *    - Button
 *    - Input
 *    - Badge
 *    - Avatar
 *    - Icon
 * 
 * 2. Molecules - Combinations of atoms
 *    - Card
 *    - Form Field
 *    - Transaction Item
 *    - Notification Item
 *    - Currency Selector
 * 
 * 3. Organisms - Complex UI sections
 *    - Header
 *    - Navigation
 *    - Transaction List
 *    - Currency Conversion Form
 *    - QR Code Display
 *    - Verification Flow
 * 
 * 4. Templates - Page layouts
 *    - Dashboard Layout
 *    - Authentication Layout
 *    - Transaction Layout
 * 
 * 5. Pages - Complete screens
 *    - Home/Dashboard
 *    - Send Money
 *    - Receive Money
 *    - Transaction History
 *    - Profile/Settings
 */

/**
 * KEY SCREENS (based on design reference)
 * --------------------------------------
 * 1. Home/Dashboard
 *    - Account balance display
 *    - Quick action buttons
 *    - Recent transaction list
 *    - Financial summary
 * 
 * 2. Send Money Flow
 *    - Recipient selection
 *    - Amount input with currency conversion
 *    - Transaction confirmation
 *    - Success/completion screen
 * 
 * 3. Receive Money
 *    - QR code display
 *    - Sharing options
 *    - Amount input (optional)
 * 
 * 4. Transaction History
 *    - Filterable list of transactions
 *    - Transaction details view
 * 
 * 5. Settings/Profile
 *    - User information
 *    - Security settings
 *    - Language preferences
 *    - Notification settings
 * 
 * 6. Authentication
 *    - Login
 *    - Registration
 *    - Verification (OTP, biometric)
 */

/**
 * INTERACTION PATTERNS
 * -------------------
 * - Smooth transitions between screens (slide, fade)
 * - Haptic feedback for important actions
 * - Pull-to-refresh for content updates
 * - Swipe gestures for common actions
 * - Bottom sheets for additional options
 * - Toast notifications for system messages
 */

/**
 * ACCESSIBILITY CONSIDERATIONS
 * ---------------------------
 * - High contrast between text and backgrounds
 * - Sufficient touch target sizes (min 44x44px)
 * - Keyboard navigation support
 * - Screen reader compatibility
 * - Respects system font size settings
 */

/**
 * RESPONSIVE DESIGN
 * ----------------
 * - Mobile-first approach
 * - Breakpoints:
 *   - sm: 640px
 *   - md: 768px
 *   - lg: 1024px
 *   - xl: 1280px
 * - Flexible layouts that adapt to different screen sizes
 * - Touch-friendly on mobile, keyboard/mouse optimized on desktop
 */
