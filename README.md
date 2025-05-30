# RemitAI - AI-Powered Remittance Platform

RemitAI is a proof-of-concept AI-powered remittance platform designed to simplify international money transfers using natural language commands (voice and text) and leveraging blockchain technology (Stellar/Soroban) for efficient, low-cost transactions.

## Project Structure

```
RemitAi/
├── backend/         # FastAPI backend code (Python 3.11)
│   ├── api/
│   ├── services/
│   ├── main.py
│   ├── requirements.txt
│   └── venv/          # Virtual environment (created locally)
├── contracts/       # Soroban smart contracts (Rust) - Not implemented in this phase
│   ├── paymaster/
│   ├── registry/
│   └── smart_wallet/
├── frontend/        # React frontend code (TypeScript + Vite + TailwindCSS)
│   ├── public/
│   ├── src/
│   ├── dist/          # Production build output (created locally)
│   ├── node_modules/  # Dependencies (installed locally)
│   ├── .env.development # Local environment config (created locally)
│   ├── .env.production  # Production environment config
│   ├── index.html
│   ├── package.json
│   ├── pnpm-lock.yaml # PNPM lock file
│   ├── tsconfig.json
│   └── vite.config.ts
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
└── README.md        # This file
```

## Features

*   **AI-Powered Interface:** Use voice or text commands (mock NLP service).
*   **Smart Wallet:** Conceptual non-custodial wallet.
*   **Gas Abstraction:** Conceptual Paymaster contract.
*   **Name Registry:** Conceptual human-readable usernames.
*   **Multi-Language Support:** Mock NLP service.
*   **Security:** Includes mock 2FA, smart wallet backup guidance, mock voice biometrics, and mock fraud detection.
*   **On/Off-Ramp:** Mock integration for buying/selling USDC.
*   **Vault Savings:** Protect local currency from depreciation by converting to USDC and locking for a specified period, earning yield while funds are locked.

## Vault Savings Feature

The Vault Savings feature allows users to protect their local currency from depreciation and inflation by:

1. **Converting local currency to USDC:** When you deposit funds into a vault, your local currency (e.g., NGN, KES) is converted to USDC at the current exchange rate.
2. **Time-locking your funds:** You choose how long to lock your funds (from 7 days to 1 year).
3. **Earning yield:** While your funds are locked, you earn interest (simulated at 5% APY).
4. **Withdrawing at current rates:** When the lock period ends, you can withdraw your funds, which are converted back to your local currency at the *current* exchange rate, protecting you from local currency depreciation.

### Benefits

* **Inflation Protection:** Shield your savings from local currency depreciation.
* **Passive Income:** Earn yield while your funds are locked.
* **Flexible Lock Periods:** Choose a timeframe that works for you (7 days to 1 year).
* **Transparent Conversion:** See exactly how much USDC your local currency converts to.
* **Automatic Unlocking:** Vaults automatically become available for withdrawal when the lock period ends.

### How to Use

1. Navigate to the Vault page from the dashboard or bottom navigation.
2. Click "New Vault" to create a new savings vault.
3. Select your local currency, enter the amount to save, and choose a lock duration.
4. Review the details and click "Create Vault".
5. Monitor your vault's status, including locked amount, yield earned, and unlock date.
6. Once unlocked, withdraw your funds to receive the equivalent amount in your local currency at the current exchange rate.

## Setup and Running Locally

These instructions guide you through setting up and running both the backend and frontend services on your local machine for development and testing.

### Prerequisites

*   **Node.js:** v20.x recommended (Check with `node -v`).
*   **pnpm:** Recommended package manager (Install via `npm install -g pnpm` if needed).
*   **Python:** v3.11.x recommended (Check with `python --version` or `python3 --version`).
*   **Git:** For cloning the repository.

### 1. Clone the Repository

```bash
git clone https://github.com/C-ifegwu/RemitAi.git
cd RemitAi
```

### 2. Setup and Run the Backend

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Create and activate a Python virtual environment:**
    ```bash
    # Use python3.11 or your python3 command
    python3.11 -m venv venv 
    
    # Activate the environment:
    # macOS / Linux:
    source venv/bin/activate
    # Windows (Git Bash or WSL):
    # source venv/Scripts/activate
    # Windows (Command Prompt / PowerShell):
    # venv\Scripts\activate.bat 
    ```
    *(You should see `(venv)` at the beginning of your terminal prompt)*

3.  **Install backend dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the backend server:**
    ```bash
    # This runs the FastAPI server using uvicorn
    # It will listen on http://127.0.0.1:8000
    # --reload enables auto-reloading on code changes
    uvicorn main:app --host 127.0.0.1 --port 8000 --reload
    ```
    *Keep this terminal window open. The backend is now running.* You should see output indicating the server is running, like `Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)`.

### 3. Setup and Run the Frontend

*(Open a **new** terminal window/tab for these steps, leaving the backend running in the first one)*

1.  **Navigate to the frontend directory:**
    ```bash
    # Make sure you are in the root RemitAi directory first
    cd frontend 
    ```
2.  **Install frontend dependencies using pnpm:**
    ```bash
    pnpm install
    ```
3.  **Configure the backend API URL for local development:**
    *   The file `.env.development` should already exist with the correct local backend URL:
        ```
        VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
        ```
    *   Verify this file exists and contains the correct URL. If not, create it and add the line above. *Note: The backend runs on port 8000, and the API routes are under `/api/v1`.*

4.  **Run the frontend development server:**
    ```bash
    pnpm run dev
    ```
5.  **Access the application:**
    *   The terminal will output the local URL for the frontend, usually `http://localhost:5173`. 
    *   Open this URL in your web browser.

### Summary

You should now have:
*   The **backend** running in one terminal (accessible at `http://127.0.0.1:8000`).
*   The **frontend** running in a second terminal (accessible at `http://localhost:5173` or similar).

You can now interact with the RemitAI application in your browser, and the frontend will communicate with your local backend.

### Building Frontend for Production

If you need to create a static build of the frontend for deployment:

1.  Navigate to the `frontend` directory: `cd frontend`
2.  Ensure your `.env.production` file has the correct `VITE_API_BASE_URL` for your *deployed* backend.
3.  Run the build command:
    ```bash
    pnpm run build
    ```
4.  The production-ready static files will be generated in the `frontend/dist` directory. Deploy these files to your preferred static hosting service.

## Contributing

Please refer to the `CONTRIBUTING.md` file for guidelines.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
