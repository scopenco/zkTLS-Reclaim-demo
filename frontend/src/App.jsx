import React, { useState } from 'react';

function App() {
  const [proofs, setProofs] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleVerification = async () => {
    setIsLoading(true);
    setError(null);
    try {
      // Step 1: Fetch the configuration from your backend
      const response = await fetch('http://localhost:3000/generate-config');
      const { reclaimProofRequestConfig } = await response.json();
      if (!reclaimProofRequestConfig) throw new Error('No config received');

      // Step 2: Dynamically import the Reclaim JS SDK
      const sdk = await import('@reclaimprotocol/js-sdk');
      const ReclaimProofRequest = sdk.ReclaimProofRequest;

      // Step 3: Initialize the ReclaimProofRequest with the received configuration
      const reclaimProofRequest = await ReclaimProofRequest.fromJsonString(reclaimProofRequestConfig);

      // Step 4: Trigger the verification flow automatically
      await reclaimProofRequest.triggerReclaimFlow();

      // Step 5: Start listening for proof submissions
      await reclaimProofRequest.startSession({
        onSuccess: (proofs) => {
          setProofs(proofs);
          setIsLoading(false);
        },
        onError: (error) => {
          setError('Verification failed: ' + error.message);
          setIsLoading(false);
        },
      });
    } catch (err) {
      setError('Error initializing Reclaim: ' + err.message);
      setIsLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: '40px auto', fontFamily: 'Arial, sans-serif' }}>
      <h1>zkTLS-Reclaim Proof Demo</h1>
      <button onClick={handleVerification} disabled={isLoading} style={{ fontSize: 18, padding: '10px 30px' }}>
        {isLoading ? 'Verifying...' : 'Start Verification'}
      </button>
      {error && <div style={{ color: 'red', marginTop: 20 }}>{error}</div>}
      {proofs && (
        <div style={{ marginTop: 30 }}>
          <h2>Verification Successful!</h2>
          <pre style={{ background: '#f4f4f4', padding: 20, borderRadius: 8 }}>{JSON.stringify(proofs, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
