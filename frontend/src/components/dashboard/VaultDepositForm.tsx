import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useForm, SubmitHandler } from 'react-hook-form';
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardFooter, 
  CardHeader, 
  CardTitle 
} from '../ui/card';
import { Input } from '../ui/input';
import { Button } from '../ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Label } from '../ui/label';
import { Slider } from '../ui/slider';
import { useVault } from '../../contexts/VaultContext';
import { useToast } from '../ui/use-toast';

interface VaultDepositFormProps {
  onSuccess?: () => void;
}

type FormValues = {
  amount: number;
  currency: string;
  duration: number;
};

const VaultDepositForm: React.FC<VaultDepositFormProps> = ({ onSuccess }) => {
  const { createVault, isLoading } = useVault();
  const { toast } = useToast();
  const [sliderValue, setSliderValue] = useState<number>(30);
  
  const { register, handleSubmit, formState: { errors }, setValue, watch } = useForm<FormValues>({
    defaultValues: {
      amount: 0,
      currency: 'NGN',
      duration: 30
    }
  });

  const watchCurrency = watch('currency');

  const handleSliderChange = (value: number[]) => {
    const newValue = value[0];
    setSliderValue(newValue);
    setValue('duration', newValue);
  };

  const getMinAmount = () => {
    return watchCurrency === 'NGN' ? 5000 : 500;
  };

  const onSubmit: SubmitHandler<FormValues> = async (data) => {
    try {
      const result = await createVault(
        data.currency,
        data.amount,
        data.duration
      );
      
      if (result) {
        toast({
          title: "Vault created successfully!",
          description: `Your ${data.currency} ${data.amount} has been securely locked for ${data.duration} days.`,
          variant: "default",
        });
        
        if (onSuccess) {
          onSuccess();
        }
      }
    } catch (error) {
      console.error('Error creating vault:', error);
      toast({
        title: "Failed to create vault",
        description: "There was an error creating your vault. Please try again.",
        variant: "destructive",
      });
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Create Savings Vault</CardTitle>
        <CardDescription>
          Protect your local currency from depreciation by converting to USDC and locking it for a specified period.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form id="vault-deposit-form" onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="currency">Currency</Label>
            <Select 
              defaultValue="NGN" 
              onValueChange={(value) => setValue('currency', value)}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select currency" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="NGN">Nigerian Naira (NGN)</SelectItem>
                <SelectItem value="KES">Kenyan Shilling (KES)</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="amount">Amount ({watchCurrency})</Label>
            <Input
              id="amount"
              type="number"
              placeholder={`Min. ${getMinAmount()}`}
              {...register('amount', { 
                required: 'Amount is required',
                min: {
                  value: getMinAmount(),
                  message: `Minimum amount is ${getMinAmount()} ${watchCurrency}`
                }
              })}
            />
            {errors.amount && (
              <p className="text-sm text-red-500">{errors.amount.message}</p>
            )}
            <p className="text-xs text-neutral-500">
              {watchCurrency === 'NGN' 
                ? 'Approx. 1 USDC = 1,500 NGN' 
                : 'Approx. 1 USDC = 130 KES'}
            </p>
          </div>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <Label htmlFor="duration">Lock Duration</Label>
              <span className="text-sm font-medium">{sliderValue} days</span>
            </div>
            <Slider
              defaultValue={[30]}
              max={365}
              min={7}
              step={1}
              onValueChange={handleSliderChange}
            />
            <div className="flex justify-between text-xs text-neutral-500">
              <span>7 days</span>
              <span>1 year</span>
            </div>
            <p className="text-xs text-neutral-500">
              Estimated yield: {(0.05 * sliderValue / 365).toFixed(2)}% ({sliderValue} days at 5% APY)
            </p>
          </div>
        </form>
      </CardContent>
      <CardFooter>
        <Button 
          type="submit" 
          form="vault-deposit-form" 
          className="w-full" 
          disabled={isLoading}
        >
          {isLoading ? 'Creating Vault...' : 'Create Vault'}
        </Button>
      </CardFooter>
    </Card>
  );
};

export default VaultDepositForm;
