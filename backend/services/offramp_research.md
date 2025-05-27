# Off-Ramp Solution Research for RemitAI

This document outlines the research conducted to select a suitable off-ramp solution for the RemitAI project. The goal is to enable users to withdraw USDC from their smart wallets and receive local fiat currency in their bank accounts or mobile money wallets across various African countries.

## Key Considerations for Off-Ramp Solutions:

*   **Geographic Coverage:** Support for target African countries (e.g., Nigeria, Kenya, Ghana).
*   **Payout Methods:** Ability to pay out to bank accounts and popular mobile money services (M-Pesa, MTN Mobile Money, Airtel Money).
*   **API Availability and Documentation:** Clear, well-documented APIs for integration.
*   **Fees and FX Rates:** Transparent and competitive fee structures and foreign exchange rates.
*   **Regulatory Compliance and KYC/AML:** Adherence to local regulations and necessary KYC/AML procedures.
*   **Reliability and Scalability:** Proven track record of service uptime and ability to handle transaction volume.
*   **Developer Experience:** Ease of integration and support for developers.
*   **Settlement Times:** Speed of fiat settlement to the end-user.
*   **USDC Support:** Direct or indirect support for USDC as the source cryptocurrency.

## Potential Off-Ramp Solutions (as per project requirements):

1.  **Stellar Anchor Platform (SEP-24 / SEP-31)**
2.  **M-Pesa API**
3.  **MTN Mobile Money API**
4.  **Flutterwave API**
5.  **Paystack API**

## Research Findings:





### 1. Stellar Anchor Platform (SEP-24 / SEP-31)

*   **Description:** Stellar provides standardized protocols (SEPs) for on/off-ramps. SEP-24 is for interactive, hosted deposit/withdrawal, while SEP-31 is for cross-border payments. Anchors are entities that connect Stellar to traditional banking.
*   **Geographic Coverage:** Depends on the specific anchor. Many anchors operate in various African countries (e.g., ClickPesa, Cowrie, Flutterwave (also an anchor), Paychant).
*   **Payout Methods:** Bank transfers, mobile money (via specific anchors).
*   **API Availability:** Yes, SEPs define the API interactions. The Anchor Platform helps deploy SEP-compliant services.
*   **Fees and FX Rates:** Varies by anchor. SEP-38 allows for RFQ (Request for Quote) to get firm quotes.
*   **Regulatory Compliance:** Anchors are responsible for their own compliance and KYC/AML according to their jurisdiction.
*   **Reliability and Scalability:** The Stellar network itself is scalable. Anchor reliability depends on the individual anchor.
*   **Developer Experience:** Good, with clear SEP documentation and tools like the Anchor Platform.
*   **Settlement Times:** Varies by anchor and payout method.
*   **USDC Support:** Yes, Stellar supports USDC (typically as a Stellar asset issued by Circle or other entities).
*   **Key SEPs for Off-Ramp:**
    *   **SEP-24 (Interactive Anchor/Wallet Withdrawals):** User is redirected to an anchor's web interface to complete withdrawal. Anchor handles KYC.
    *   **SEP-31 (Cross-Border Payments):** Designed for businesses sending payments. Requires more direct integration and often bilateral agreements. Anchor handles KYC of the *receiving* customer.
    *   **SEP-6 (Programmatic Deposit/Withdrawal):** Wallet collects KYC and interacts directly with anchor APIs. Less common for pure off-ramps due to KYC burden on wallets.
    *   **SEP-12 (KYC API):** Standard for wallets to provide KYC info to anchors if needed (more relevant for SEP-6).
    *   **SEP-38 (Anchor RFQ API):** Allows getting a firm quote for currency conversion before initiating a transaction.

*   **Conclusion for RemitAI:** Promising, especially if leveraging existing anchors in target countries. SEP-24 seems most suitable for user-initiated withdrawals. Requires identifying and integrating with specific anchors. Could offer a decentralized and potentially lower-cost option if good anchors are available.



### 2. M-Pesa API (Safaricom Daraja API)

*   **Description:** M-Pesa is a dominant mobile money service in East Africa, particularly Kenya. Safaricom provides the Daraja API for developers to integrate with M-Pesa services.
*   **Geographic Coverage:** Primarily Kenya, with presence in Tanzania (Vodacom M-Pesa), Mozambique, DRC, Lesotho, Ghana, and Egypt. Direct API integration is typically country-specific (e.g., Safaricom for Kenya).
*   **Payout Methods:** Direct to M-Pesa mobile wallets.
*   **API Availability:** Yes, Safaricom offers the Daraja API. It includes various functionalities like Business to Customer (B2C) payments, which is relevant for off-ramping.
*   **Fees and FX Rates:** Transaction fees apply as per Safaricom's M-Pesa tariffs. FX conversion would typically happen before initiating an M-Pesa payout if the source is not KES.
*   **Regulatory Compliance:** Safaricom is a regulated entity. Businesses integrating would need to comply with Safaricom's terms and local regulations, including KYC/AML for their own services.
*   **Reliability and Scalability:** M-Pesa is a highly reliable and scalable platform within its operating countries.
*   **Developer Experience:** Safaricom provides a developer portal with API documentation and sandbox environments. Integration can be complex due to specific security requirements and approval processes.
*   **Settlement Times:** Payouts to M-Pesa wallets are typically instant or near-instant once processed.
*   **USDC Support:** No direct USDC support within M-Pesa itself. Conversion from USDC to KES (or other local currency) would need to happen via an exchange or liquidity provider before initiating an M-Pesa B2C payout.

*   **Conclusion for RemitAI:** A strong candidate for off-ramping in Kenya and other M-Pesa dominant countries. The primary challenge is the USDC to local currency conversion step, which would need to be handled by RemitAI or a partner before using the M-Pesa API for the final payout. Direct integration with Daraja API is feasible for B2C payouts.



### 3. MTN Mobile Money (MoMo) API

*   **Description:** MTN is a major telecommunications provider across Africa, and its Mobile Money (MoMo) service is widely used. MTN provides the MoMo API for developers to integrate various financial services.
*   **Geographic Coverage:** Extensive coverage in many African countries where MTN operates (e.g., Nigeria, Ghana, Uganda, Ivory Coast, Cameroon, Benin, Rwanda, Zambia, etc.).
*   **Payout Methods:** Direct to MTN MoMo wallets.
*   **API Availability:** Yes, MTN offers the MoMo Developer Portal with API documentation (e.g., for Collections, Disbursements, Remittances).
*   **Fees and FX Rates:** Transaction fees are applicable as per MTN MoMo tariffs for the specific country. FX conversion from USDC to local currency would need to be handled externally before initiating a MoMo payout.
*   **Regulatory Compliance:** MTN is a regulated entity in its countries of operation. Integrating businesses must comply with MTN’s terms and local financial regulations.
*   **Reliability and Scalability:** MTN MoMo is generally a reliable and scalable platform within its operational countries.
*   **Developer Experience:** MTN provides a developer portal with API documentation, SDKs (e.g., Java, PHP, Python), and a sandbox environment. Integration complexity can vary by country and specific API product.
*   **Settlement Times:** Payouts to MoMo wallets are typically instant or near-instant.
*   **USDC Support:** No direct USDC support within the MoMo API. Conversion from USDC to local currency is a prerequisite for using the API for fiat payouts.

*   **Conclusion for RemitAI:** A strong candidate for off-ramping in countries with high MTN MoMo penetration. Similar to M-Pesa, the main challenge is the USDC to local currency conversion step, which RemitAI or a partner would need to manage before using the MoMo API for the final disbursement. The Disbursements API product would be relevant here.


### 4. Flutterwave API

*   **Description:** Flutterwave is a leading African fintech company providing payment infrastructure for global merchants and payment service providers across the continent. They offer a comprehensive suite of payment APIs.
*   **Geographic Coverage:** Extensive coverage across Africa, including Nigeria, Ghana, Kenya, South Africa, Uganda, Tanzania, and many other countries.
*   **Payout Methods:** Bank transfers, mobile money (including M-Pesa, MTN MoMo, Airtel Money), and other local payment methods.
*   **API Availability:** Yes, Flutterwave offers well-documented APIs for various payment operations, including their Transfers API for disbursements.
*   **Fees and FX Rates:** Transaction fees vary by country and payment method. Flutterwave typically handles FX conversion with competitive rates.
*   **Regulatory Compliance:** Flutterwave is a regulated entity in multiple African countries and complies with local financial regulations. Businesses integrating with Flutterwave must also comply with relevant regulations.
*   **Reliability and Scalability:** Flutterwave has a proven track record of reliability and scalability, processing millions of transactions.
*   **Developer Experience:** Good developer experience with comprehensive documentation, SDKs (e.g., Node.js, PHP, Python), and support.
*   **Settlement Times:** Varies by country and payment method, but generally within 24 hours for most destinations.
*   **USDC Support:** Recent developments indicate Flutterwave is partnering with Circle (USDC issuer) to enable stablecoin payments across Africa, potentially making it a direct on/off-ramp for USDC.

*   **Conclusion for RemitAI:** A strong candidate for off-ramping across multiple African countries due to its extensive coverage and support for various local payment methods. The potential direct USDC integration makes it particularly interesting for RemitAI's use case, potentially simplifying the conversion step from USDC to local currency.



### 5. Paystack API

*   **Description:** Paystack is another prominent African payment gateway, acquired by Stripe. It offers a range of payment processing tools for businesses in Africa.
*   **Geographic Coverage:** Strong presence in Nigeria, Ghana, South Africa, and expanding to other African countries.
*   **Payout Methods:** Bank transfers, mobile money (in some regions).
*   **API Availability:** Yes, Paystack provides well-documented APIs for payments and transfers.
*   **Fees and FX Rates:** Competitive transaction fees, which vary by country. FX conversion is handled by Paystack.
*   **Regulatory Compliance:** Paystack adheres to local financial regulations and PCI-DSS standards.
*   **Reliability and Scalability:** Known for reliability and used by many businesses, backed by Stripe's infrastructure.
*   **Developer Experience:** Excellent developer experience with clear documentation, SDKs, and a supportive community.
*   **Settlement Times:** Typically next-day settlement for bank transfers, mobile money can be faster.
*   **USDC Support:** Not a primary focus for direct crypto on/off-ramping. Would likely require external conversion of USDC to fiat before using Paystack for payouts.

*   **Conclusion for RemitAI:** A very strong option for fiat payouts in its supported countries, especially Nigeria and Ghana, due to its robust platform and developer-friendly APIs. Similar to M-Pesa and MTN, USDC conversion would be an external step.

## Overall Conclusion and Recommended Strategy for RemitAI Off-Ramp:

After reviewing the available options, a hybrid approach is recommended for RemitAI to achieve broad coverage and flexibility:

1.  **Primary Recommendation: Flutterwave.**
    *   **Reasoning:** Flutterwave offers the broadest geographical coverage across Africa, supports a wide array of payout methods (bank, mobile money), and is actively moving towards direct USDC support through its partnership with Circle. This aligns well with RemitAI's need to off-ramp USDC directly to local fiat currencies.
    *   **Implementation:** Prioritize integration with Flutterwave's Transfers API, and monitor their USDC off-ramp capabilities as they become available.

2.  **Secondary/Complementary Options:**
    *   **Stellar Anchor Platform (SEP-24):** For specific corridors where well-established and cost-effective Stellar anchors exist, SEP-24 integration can provide a decentralized and potentially lower-cost alternative. This would require identifying and vetting individual anchors.
    *   **Direct Mobile Money APIs (M-Pesa, MTN MoMo):** In countries where these services are dominant and Flutterwave might have gaps or less competitive rates, direct integration could be considered. However, this adds complexity due to managing multiple direct integrations and handling USDC-to-fiat conversion separately for each.
    *   **Paystack:** A strong alternative to Flutterwave in its core markets (Nigeria, Ghana, SA) if Flutterwave integration faces challenges or for diversification.

3.  **Mock Implementation First:** For initial development and testing, a mock off-ramp service will be implemented. This mock service will simulate interactions with a provider like Flutterwave, allowing the frontend and core logic to be built and tested independently of live API integrations.

**Next Steps:**

*   Implement a mock `OffRampService` in Python, mirroring the structure of the `OnRampService`.
*   This service will simulate initiating a withdrawal (USDC to Fiat), checking status, and providing mock payout details.
*   Once the core application logic is stable, proceed with integrating a live API, starting with Flutterwave (or its sandbox environment if available for USDC off-ramping).
