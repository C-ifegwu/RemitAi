import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { useAuth } from '../contexts/AuthContext';
import { ShieldCheck, Mail } from 'lucide-react';

const VerifyIdentity: React.FC = () => {
  const [otp, setOtp] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  // Use verifyOTP (correct name) and user from context
  const { verifyOTP, user } = useAuth(); 
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!otp || otp.length !== 6) {
      setError('Please enter a valid 6-digit OTP.');
      return;
    }

    if (!user || !user.id) { // Ensure user and user.id are available
      setError('User information not found. Please log in again.');
      return;
    }

    setIsLoading(true);
    try {
      // Call verifyOTP with userId and otpCode
      await verifyOTP(user.id, otp); 
      // On successful verification, navigate to the dashboard
      navigate('/');
    } catch (err: any) {
      setError(err.message || 'OTP verification failed. Please check the code and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleResendOtp = async () => {
    // Add logic to resend OTP
    console.log('Resend OTP requested');
    // You might call an API endpoint here, e.g., authAPI.requestOtp(user?.id, user?.phoneNumber, 'sms')
    alert('A new OTP has been sent (simulation).');
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-md mx-auto p-8 space-y-6 bg-card rounded-xl shadow-lg"
    >
      <div className="text-center">
        <ShieldCheck className="mx-auto h-12 w-12 text-primary mb-4" />
        <h1 className="text-3xl font-bold text-foreground">Verify Your Identity</h1>
        <p className="text-muted-foreground">
          Enter the 6-digit code sent to your email {user?.email ? `(${user.email})` : ''}.
        </p>
      </div>

      {error && (
        <div className="bg-destructive/10 border border-destructive/20 text-destructive px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <Label htmlFor="otp">Verification Code</Label>
          <div className="relative mt-1">
            <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              id="otp"
              type="text"
              placeholder="Enter 6-digit code"
              value={otp}
              onChange={(e) => setOtp(e.target.value.replace(/[^0-9]/g, '').slice(0, 6))}
              required
              maxLength={6}
              className="pl-10 tracking-[0.3em] text-center"
            />
          </div>
        </div>

        <Button type="submit" className="w-full" disabled={isLoading}>
          {isLoading ? (
            <>
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Verifying...
            </>
          ) : (
            'Verify Code'
          )}
        </Button>
      </form>

      <p className="text-center text-sm text-muted-foreground">
        Didn't receive the code?{' '}
        <button onClick={handleResendOtp} className="font-medium text-primary hover:underline">
          Resend Code
        </button>
      </p>
    </motion.div>
  );
};

export default VerifyIdentity;

