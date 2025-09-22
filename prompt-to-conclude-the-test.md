### **Prompt: Diagnostic Test Plan for OCI Function VCN Integration**

**Objective (The "Why"):**

The primary objective of this test is to definitively isolate a suspected platform-level bug within the OCI Functions service. Our main application, `rag-ingestor`, is consistently failing with a `FunctionInvokeSubnetNotAvailable (502)` error, which suggests the platform cannot prepare the function's network environment.

We hypothesize that this failure is **not related to our application's code, dependencies, or complexity**, but is a fundamental issue with VCN integration for any function in our environment. This test will prove or disprove that hypothesis using a minimal, clean-room function.

**Test Subject:**

*   **Function Name:** `vcn-diagnostic-fn`
*   **Application:** `rag-app`
*   **Characteristics:** This is a bare-bones Python function with a single dependency (`fdk`). It contains no logic for connecting to databases, fetching secrets, or parsing complex events. Its sole purpose is to successfully initialize within a VCN.
*   **Configuration:** The parent application, `rag-app`, has been re-created and is correctly configured to place all its functions within the private subnet `ocid1.subnet.oc1.eu-frankfurt-1...ku6a`.

**Expected Outcome (The Hypothesis):**

We expect this test to **FAIL**.

The successful execution of this test plan will result in the `vcn-diagnostic-fn` invocation failing with the exact same error as our main application: `FunctionInvokeSubnetNotAvailable (502)`.

This "successful failure" is the critical piece of evidence needed to prove to Oracle Support that the issue lies within their platform, not our code.

**Execution Steps:**

1.  **Confirm Prerequisites:**
    *   Verify that the `rag-app` application exists and is configured with the correct private subnet OCID.
    *   Verify that the `vcn-diagnostic-fn` has been successfully deployed to the `rag-app`.

2.  **Invoke the Diagnostic Function:**
    *   Execute the following command from the OCI CLI to trigger the function:
        ```bash
        fn invoke rag-app vcn-diagnostic-fn
        ```

3.  **Retrieve and Analyze the Logs:**
    *   Wait approximately 60 seconds for the invocation to complete and logs to be ingested.
    *   First, retrieve the unique OCID of the diagnostic function:
        ```bash
        oci fn function get --application-id <rag-app-ocid> --function-name vcn-diagnostic-fn --query "data.id"
        ```
    *   Next, execute the following OCI CLI command to search for the specific logs from this invocation. Replace the placeholders with your values.
        ```bash
        # --- OCI Logging Search Command ---
        # Replace <TENANCY_OCID>, <LOG_OCID>, and <DIAGNOSTIC_FN_OCID>

        TIME_START=$(date --iso-8601=seconds --date="5 minutes ago")

        oci logging-search search-logs \
        --compartment-id "<TENANCY_OCID>" \
        --search-query "search \"<LOG_OCID>\" | where data.functionId = '<DIAGNOSTIC_FN_OCID>' | sort by datetime desc" \
        --time-start "$TIME_START"
        ```

**Result Analysis and Conclusion:**

Please analyze the log output and provide a conclusion based on the following criteria:

*   **Conclusion 1: Hypothesis Confirmed (Expected Failure)**
    *   **Condition:** The logs show a `502` error with the message `FunctionInvokeSubnetNotAvailable`.
    *   **Action:** This is a successful test. Extract the new `opc-request-id` from the internal `GetSubnet` call failure within the error message. Conclude that the platform is at fault and the next step is to update the Oracle Support ticket with this clean, undeniable evidence.

*   **Conclusion 2: Hypothesis Rejected (Unexpected Success)**
    *   **Condition:** The logs show a successful invocation, including the message "VCN Diagnostic Function executed."
    *   **Action:** This would be a surprising result. Conclude that our hypothesis was incorrect and the issue is, in fact, specific to the `rag-ingestor` function. The next step would be a deep-dive comparison of the `rag-ingestor` function's image, dependencies, or configuration against this working baseline.

*   **Conclusion 3: Different Error**
    *   **Condition:** The logs show a new and different error message.
    *   **Action:** Document the new error in detail. Conclude that while the initial hypothesis may be incorrect, there is still an underlying issue that needs to be diagnosed. Provide the full log output for further analysis.
