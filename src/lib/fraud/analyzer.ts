export interface FraudAnalysisResult {
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  riskScore: number; // 0 to 100
  category: string;
  reasons: string[];
  reasonsKn: string[];
  recommendation: string;
  recommendationKn: string;
  isPhishing: boolean;
  isSandbox: true;
}

export function analyzeFraudRisk(inputText: string): FraudAnalysisResult {
  const text = inputText.toLowerCase();
  const reasons: string[] = [];
  const reasonsKn: string[] = [];
  let score = 10; // baseline safe score

  // Detect sensitive banking terms & OTP requests
  if (text.includes('otp') || text.includes('pin') || text.includes('password') || text.includes('cvv') || text.includes('account number')) {
    score += 50;
    reasons.push('Message requests confidential banking information (OTP / PIN / Password).');
    reasonsKn.push('ಸಂದೇಶವು ಗೌಪ್ಯ ಬ್ಯಾಂಕಿಂಗ್ ಮಾಹಿತಿಯನ್ನು (OTP / PIN) ಕೇಳುತ್ತಿದೆ.');
  }

  // Detect suspicious links
  if (text.includes('http') || text.includes('.bit.ly') || text.includes('click') || text.includes('t.co') || text.includes('claim')) {
    score += 35;
    reasons.push('Contains unverified external link or suspicious URL.');
    reasonsKn.push('ಪರಿಶೀಲಿಸದ ಬಾಹ್ಯ ಲಿಂಕ್ ಅಥವಾ ಅನುಮಾನಾಸ್ಪದ ಯುಆರ್‌ಎಲ್ ಹೊಂದಿದೆ.');
  }

  // Detect fake urgent loan / subsidy approval scams
  if (text.includes('approved') || text.includes('immediate') || text.includes('subsidy claim') || text.includes('urgent') || text.includes('lottery') || text.includes('pm-kisan cash')) {
    score += 25;
    reasons.push('Uses high-pressure tactics or fake urgent financial approval claims.');
    reasonsKn.push('ತಕ್ಷಣದ ಸಾಲ ಅಥವಾ ಸಬ್ಸಿಡಿ ಮಂಜೂರಾತಿಯ ನಕಲಿ ಭರವಸೆ ನೀಡುತ್ತಿದೆ.');
  }

  let riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' = 'LOW';
  let category = 'Legitimate Notification';
  let recommendation = 'No immediate threat detected. Always verify through official Bank/Govt counters.';
  let recommendationKn = 'ಯಾವುದೇ ತಕ್ಷಣದ ಅಪಾಯ ಕಂಡುಬಂದಿಲ್ಲ. ಅಧಿಕೃತ ಶಾಖೆಯಲ್ಲಿ ಪರಿಶೀಲಿಸಿ.';

  if (score >= 75) {
    riskLevel = 'HIGH';
    category = 'Phishing / Banking Fraud';
    recommendation = 'HIGH RISK! Do NOT click links. Never share OTP/PIN with anyone.';
    recommendationKn = 'ಹೆಚ್ಚಿನ ಅಪಾಯ! ಲಿಂಕ್ ಕ್ಲಿಕ್ ಮಾಡಬೇಡಿ. ಯಾರೊಂದಿಗೂ OTP ಹಂಚಿಕೊಳ್ಳಬೇಡಿ.';
  } else if (score >= 45) {
    riskLevel = 'MEDIUM';
    category = 'Suspicious Scheme Offer';
    recommendation = 'Proceed with caution. Cross-check scheme status on KisanKavach benefits tab.';
    recommendationKn = 'ಎಚ್ಚರಿಕೆಯಿಂದ ಇರಿ. ಕಿಸಾನ್‌ಕವಚ ಸೌಲಭ್ಯಗಳ ವಿಭಾಗದಲ್ಲಿ ಪರಿಶೀಲಿಸಿ.';
  }

  return {
    riskLevel,
    riskScore: Math.min(100, score),
    category,
    reasons: reasons.length > 0 ? reasons : ['Clean text pattern matching official template.'],
    reasonsKn: reasonsKn.length > 0 ? reasonsKn : ['ಅಧಿಕೃತ ಮಾದರಿಗೆ ಸೂಕ್ತವಾದ ಉಲ್ಲೇಖ.'],
    recommendation,
    recommendationKn,
    isPhishing: score >= 60,
    isSandbox: true,
  };
}
