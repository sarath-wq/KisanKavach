export interface SandboxFarmerProfile {
  fruitsId: string;
  farmerName: string;
  aadhaarMasked: string;
  district: string;
  taluk: string;
  village: string;
  totalLandAcres: number;
  verificationStatus: 'VERIFIED' | 'PENDING' | 'REJECTED';
  isSandbox: true;
}

export interface SandboxLandRecord {
  bhoomiRtcId: string;
  surveyNumber: string;
  hissaNumber: string;
  villageName: string;
  extentAcres: number;
  ownerName: string;
  landType: string;
  soilType: string;
  isSandbox: true;
}

export interface SandboxCropData {
  cropName: string;
  cropNameKn: string;
  season: string;
  surveyNumber: string;
  areaAcres: number;
  expectedYieldQuintals: number;
  isSandbox: true;
}

export interface SandboxCreditStatus {
  cibilScore: number;
  existingLoansCount: number;
  totalOutstandings: number;
  defaultHistory: boolean;
  recommendation: 'ELIGIBLE_FOR_KCC' | 'CONDITIONAL' | 'HIGH_RISK';
  isSandbox: true;
}

export interface SandboxInsurancePolicy {
  policyNumber: string;
  crop: string;
  season: string;
  year: number;
  sumInsured: number;
  premiumPaid: number;
  status: string;
  claimStatus: string;
  isSandbox: true;
}

export interface SandboxWeatherAlert {
  id: string;
  district: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  headline: string;
  headlineKn: string;
  advisory: string;
  advisoryKn: string;
  timestamp: string;
  isSandbox: true;
}

// Integration Interfaces
export interface FarmerRegistryProvider {
  getFarmerProfile(farmerId: string): Promise<SandboxFarmerProfile>;
}

export interface LandRecordProvider {
  getLandRecords(farmerId: string): Promise<SandboxLandRecord[]>;
}

export interface CropProvider {
  getCropData(farmerId: string): Promise<SandboxCropData[]>;
}

export interface CreditProvider {
  getCreditStatus(farmerId: string): Promise<SandboxCreditStatus>;
}

export interface WeatherProvider {
  getWeatherRiskAlerts(districtName: string): Promise<SandboxWeatherAlert[]>;
}

// Sandbox Adapters Implementations
export class MockFarmerRegistryAdapter implements FarmerRegistryProvider {
  async getFarmerProfile(farmerId: string): Promise<SandboxFarmerProfile> {
    return {
      fruitsId: `FRUITS-KA-2026-${farmerId.slice(0, 6)}`,
      farmerName: 'Ramesh Gowda',
      aadhaarMasked: 'XXXX-XXXX-4821',
      district: 'Mysuru',
      taluk: 'Nanjangud',
      village: 'Hullahalli',
      totalLandAcres: 3.5,
      verificationStatus: 'VERIFIED',
      isSandbox: true,
    };
  }
}

export class MockLandRecordAdapter implements LandRecordProvider {
  async getLandRecords(farmerId: string): Promise<SandboxLandRecord[]> {
    return [
      {
        bhoomiRtcId: 'RTC-KA-MYS-142/1A',
        surveyNumber: '142/1A',
        hissaNumber: '1A',
        villageName: 'Hullahalli',
        extentAcres: 2.0,
        ownerName: 'Ramesh Gowda',
        landType: 'Dry Agricultural',
        soilType: 'Red Loamy',
        isSandbox: true,
      },
      {
        bhoomiRtcId: 'RTC-KA-MYS-142/2B',
        surveyNumber: '142/2B',
        hissaNumber: '2B',
        villageName: 'Hullahalli',
        extentAcres: 1.5,
        ownerName: 'Ramesh Gowda',
        landType: 'Irrigated Agricultural',
        soilType: 'Black Cotton',
        isSandbox: true,
      },
    ];
  }
}

export class MockCropAdapter implements CropProvider {
  async getCropData(farmerId: string): Promise<SandboxCropData[]> {
    return [
      {
        cropName: 'Ragi (Finger Millet)',
        cropNameKn: 'ರಾಗಿ',
        season: 'Kharif',
        surveyNumber: '142/1A',
        areaAcres: 2.0,
        expectedYieldQuintals: 24,
        isSandbox: true,
      },
      {
        cropName: 'Paddy (Rice)',
        cropNameKn: 'ಭತ್ತ',
        season: 'Kharif',
        surveyNumber: '142/2B',
        areaAcres: 1.5,
        expectedYieldQuintals: 30,
        isSandbox: true,
      },
    ];
  }
}

export class MockCreditAdapter implements CreditProvider {
  async getCreditStatus(farmerId: string): Promise<SandboxCreditStatus> {
    return {
      cibilScore: 742,
      existingLoansCount: 0,
      totalOutstandings: 0,
      defaultHistory: false,
      recommendation: 'ELIGIBLE_FOR_KCC',
      isSandbox: true,
    };
  }
}

export class MockWeatherAdapter implements WeatherProvider {
  async getWeatherRiskAlerts(districtName: string): Promise<SandboxWeatherAlert[]> {
    return [
      {
        id: 'W-KA-MYS-001',
        district: districtName || 'Mysuru',
        severity: 'HIGH',
        headline: 'Heavy Rainfall & Pest Infestation Warning',
        headlineKn: 'ಭಾರಿ ಮಳೆ ಮತ್ತು ಕೀಟ ಬಾಧೆಯ ಮುನ್ನೆಚ್ಚರಿಕೆ',
        advisory: 'KSNDMC forecasts 75mm heavy rain in next 48h. Secure harvested Ragi and inspect Paddy drainage.',
        advisoryKn: 'ಮುಂದಿನ 48 ಗಂಟೆಗಳಲ್ಲಿ 75ಮಿಮೀ ಭಾರಿ ಮಳೆಯಾಗುವ ಸಾಧ್ಯತೆಯಿದೆ. ಕೊಯ್ಲು ಮಾಡಿದ ಬೆಳೆಗಳನ್ನು ಸುರಕ್ಷಿತವಾಗಿರಿಸಿ.',
        timestamp: new Date().toISOString(),
        isSandbox: true,
      },
    ];
  }
}

// Singletons
export const fruitsAdapter = new MockFarmerRegistryAdapter();
export const bhoomiAdapter = new MockLandRecordAdapter();
export const cropAdapter = new MockCropAdapter();
export const creditAdapter = new MockCreditAdapter();
export const weatherAdapter = new MockWeatherAdapter();
