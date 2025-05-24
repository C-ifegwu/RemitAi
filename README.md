# RemitAI - AI-Powered Remittance Platform

RemitAI is a proof-of-concept AI-powered remittance platform designed to simplify international money transfers using natural language commands (voice and text) and leveraging blockchain technology (Stellar/Soroban) for efficient, low-cost transactions.

## Project Structure

```
RemitAi/
├── backend/         # FastAPI backend code (Python)
│   ├── api/
│   ├── services/
│   ├── main.py
│   └── requirements.txt
├── contracts/       # Soroban smart contracts (Rust)
│   ├── paymaster/
│   ├── registry/
│   └── smart_wallet/
├── frontend/        # React frontend code (TypeScript + Vite + TailwindCSS)
│   ├── public/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
└── README.md        # This file
```

## Features

*   **AI-Powered Interface:** Use voice or text commands in multiple languages to initiate transfers.
*   **Smart Wallet:** Non-custodial smart contract wallet on Soroban.
*   **Gas Abstraction:** Paymaster contract sponsors transaction fees.
*   **Name Registry:** Human-readable usernames linked to wallet addresses.
*   **Multi-Language Support:** NLP understands commands in English, Swahili, Yoruba, Hausa, Igbo, French, Arabic.
*   **Security:** Includes 2FA, smart wallet backup, voice biometrics (mock), and fraud detection.
*   **On/Off-Ramp:** Mock integration for buying/selling USDC.

## Setup and Running

### Prerequisites

*   Node.js (v20 or later recommended)
*   npm, yarn, or pnpm (pnpm is recommended as used during development)
*   Python (v3.9 or later recommended for backend)
*   Rust toolchain (for Soroban contracts)

### Backend Setup (Placeholder - Details in `backend/README.md` if available)

1.  Navigate to the `backend` directory: `cd backend`
2.  Create a virtual environment: `python -m venv venv`
3.  Activate the virtual environment:
    *   macOS/Linux: `source venv/bin/activate`
    *   Windows: `venv\Scripts\activate`
4.  Install dependencies: `pip install -r requirements.txt`
5.  Configure environment variables (e.g., API keys, database connection) in a `.env` file.
6.  Run the backend server: `uvicorn main:app --reload`

### Frontend Setup

1.  Navigate to the `frontend` directory: `cd frontend`
2.  Install dependencies (using pnpm is recommended):
    ```bash
    pnpm install
    ```
    *Alternatively, use npm or yarn:*
    ```bash
    # npm install
    # or
    # yarn install
    ```
3.  **Configure Backend API URL:**
    *   Create a `.env.development` file in the `frontend` directory.
    *   Add the following line, replacing the URL with your running backend server's address:
        ```
VITE_API_BASE_URL=http://localhost:8000/api/v1
        ```
    *   For production builds, ensure the `VITE_API_BASE_URL` is set correctly in your deployment environment or in a `.env.production` file.

4.  **Run the Frontend Development Server:**
    ```bash
    pnpm run dev
    ```
    *Alternatively, use npm or yarn:*
    ```bash
    # npm run dev
    # or
    # yarn dev
    ```
5.  Open your browser and navigate to the URL provided (usually `http://localhost:5173`).

### Building for Production

1.  Navigate to the `frontend` directory: `cd frontend`
2.  Run the build command:
    ```bash
    pnpm run build
    ```
    *Alternatively, use npm or yarn:*
    ```bash
    # npm run build
    # or
    # yarn build
    ```
3.  The production-ready static files will be generated in the `frontend/dist` directory. Deploy these files to your preferred static hosting service (e.g., Vercel, Netlify, GitHub Pages).

## Contributing

Please refer to the `CONTRIBUTING.md` file for guidelines.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

