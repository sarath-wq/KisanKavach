import { prisma } from '../db/prisma';

export interface AIResponse {
  answer: string;
  answerKn: string;
  suggestedActions?: { label: string; href: string }[];
  isSandbox: true;
}

export async function askKisanAI(farmerUserId: string, question: string): Promise<AIResponse> {
  const query = question.toLowerCase();

  // Fetch authorized farmer context
  const farmer = await prisma.farmer.findFirst({
    where: { userId: farmerUserId },
    include: {
      applications: { orderBy: { submittedAt: 'desc' }, take: 1, include: { bankBranch: { include: { bank: true } } } },
      benefits: { include: { scheme: true } },
      policies: true,
      grievances: { orderBy: { createdAt: 'desc' }, take: 1 },
    },
  });

  const latestApp = farmer?.applications[0];
  const activeGrievance = farmer?.grievances[0];

  // Intent 1: KCC Application Status
  if (query.includes('kcc') || query.includes('status') || query.includes('application') || query.includes('loan') || query.includes('ಸಾಲ') || query.includes('ಅರ್ಜಿ')) {
    if (latestApp) {
      const stage = latestApp.currentStage.replace(/_/g, ' ');
      const bank = latestApp.bankBranch.bank.name;
      const isBreached = latestApp.slaBreached;

      const answer = `Your KCC Application (${latestApp.applicationId}) is currently in stage: "${stage}" at ${bank} (${latestApp.bankBranch.branchName}). Status: ${latestApp.status}. ${isBreached ? '⚠️ Note: Processing has exceeded normal SLA days.' : 'No action required from you right now.'}`;
      
      const answerKn = `ನಿಮ್ಮ ಕೆ.ಸಿ.ಸಿ ಸಾಲ ಅರ್ಜಿ (${latestApp.applicationId}) ಪ್ರಸ್ತುತ "${stage}" ಹಂತದಲ್ಲಿದೆ. ಬ್ಯಾಂಕ್: ${bank}. ಸ್ಥಿತಿ: ${latestApp.status}. ${isBreached ? '⚠️ ಗಮನಿಸಿ: ನಿಗದಿತ ಸಮಯಕ್ಕಿಂತ ವಿಳಂಬವಾಗಿದೆ.' : 'ನಿಮ್ಮಿಂದ ಯಾವುದೇ ಹೆಚ್ಚಿನ ಕ್ರಮದ ಅಗತ್ಯವಿಲ್ಲ.'}`;

      return {
        answer,
        answerKn,
        suggestedActions: [
          { label: 'Track KCC Application', href: `/farmer/kcc/${latestApp.id}` },
          ...(isBreached ? [{ label: 'Raise SLA Grievance', href: '/farmer/grievances/new' }] : []),
        ],
        isSandbox: true,
      };
    } else {
      return {
        answer: 'You have not submitted a KCC Application yet. You can apply directly through KisanKavach with 1-click Bhoomi land verification.',
        answerKn: 'ನೀವು ಇನ್ನು ಕೆ.ಸಿ.ಸಿ ಸಾಲಕ್ಕೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಿಲ್ಲ. ಕಿಸಾನ್‌ಕವಚ ಮೂಲಕ ತಕ್ಷಣ ಅರ್ಜಿ ಸಲ್ಲಿಸಬಹುದು.',
        suggestedActions: [{ label: 'Apply For KCC Loan', href: '/farmer/kcc/new' }],
        isSandbox: true,
      };
    }
  }

  // Intent 2: Benefits Eligibility
  if (query.includes('benefit') || query.includes('scheme') || query.includes('pm-kisan') || query.includes('ಯೋಜನೆ') || query.includes('ಸೌಲಭ್ಯ')) {
    const benefitCount = farmer?.benefits.length || 0;
    return {
      answer: `Based on your land records (${farmer?.landSizeAcres || 3.5} acres in ${farmer?.districtId || 'Mysuru'}), you are currently linked to ${benefitCount} Government schemes including PM-KISAN and PMFBY Crop Insurance.`,
      answerKn: `ನಿಮ್ಮ ಜಮೀನಿನ ವಿವರಗಳ ಆಧಾರದ ಮೇಲೆ (${farmer?.landSizeAcres || 3.5} ಎಕರೆ), ನೀವು ಪಿಎಂ-ಕಿಸಾನ್ ಹಾಗೂ ಪ್ರಧಾನ್ ಮಂತ್ರಿ ಫಸಲ್ ಭೀಮಾ ಯೋಜನೆ ಸೇರಿದಂತೆ ${benefitCount} ಸರ್ಕಾರಿ ಸೌಲಭ್ಯಗಳಿಗೆ ಅರ್ಹರಾಗಿದ್ದೀರಿ.`,
      suggestedActions: [{ label: 'View My Benefits', href: '/farmer/benefits' }],
      isSandbox: true,
    };
  }

  // Intent 3: Complaint / Grievance
  if (query.includes('complaint') || query.includes('grievance') || query.includes('delay') || query.includes('ದೂರು') || query.includes('ವಿಳಂಬ')) {
    if (activeGrievance) {
      return {
        answer: `Your grievance (${activeGrievance.grievanceId}) regarding "${activeGrievance.subject}" is currently "${activeGrievance.status}". Assigned Officer is reviewing the case.`,
        answerKn: `ನಿಮ್ಮ ದೂರು (${activeGrievance.grievanceId}) "${activeGrievance.subject}" ಪ್ರಸ್ತುತ "${activeGrievance.status}" ಹಂತದಲ್ಲಿದೆ. ನಿಯೋಜಿತ ಅಧಿಕಾರಿಯು ಪರಿಶೀಲಿಸುತ್ತಿದ್ದಾರೆ.`,
        suggestedActions: [{ label: 'Track Grievance', href: `/farmer/grievances/${activeGrievance.id}` }],
        isSandbox: true,
      };
    }
    return {
      answer: 'If your KCC application is delayed or if you face bank/subsidy issues, you can register an official grievance directly escalated to the District Officer.',
      answerKn: 'ನಿಮ್ಮ ಸಾಲ ವಿಳಂಬವಾಗಿದ್ದರೆ ಅಥವಾ ಸೌಲಭ್ಯ ಸಿಗದಿದ್ದರೆ ನೇರವಾಗಿ ಜಿಲ್ಲಾಧಿಕಾರಿಗಳಿಗೆ ದೂರು ಸಲ್ಲಿಸಬಹುದು.',
      suggestedActions: [{ label: 'Register New Grievance', href: '/farmer/grievances/new' }],
      isSandbox: true,
    };
  }

  // Intent 4: Fraud / Scam verification
  if (query.includes('fraud') || query.includes('sms') || query.includes('link') || query.includes('message') || query.includes('ನಕಲಿ') || query.includes('ಸಂದೇಶ')) {
    return {
      answer: 'You can test any suspicious SMS, WhatsApp message, or website link using the Cyber Kavach tool to check for phishing or bank fraud risk.',
      answerKn: 'ಯಾವುದೇ ಅನುಮಾನಾಸ್ಪದ ಸಂದೇಶ ಅಥವಾ ಲಿಂಕ್ ಅನ್ನು ಸೈಬರ್ ಕವಚ ಉಪಕರಣದ ಮೂಲಕ ಉಚಿತವಾಗಿ ಪರಿಶೀಲಿಸಬಹುದು.',
      suggestedActions: [{ label: 'Open Cyber Kavach', href: '/farmer/fraud' }],
      isSandbox: true,
    };
  }

  // Default General Assistant Response
  return {
    answer: 'Namaskara! I am your KisanKavach Assistant. I can help you check your KCC loan status, discover eligible Government schemes, monitor crop insurance claims, or verify suspicious SMS messages.',
    answerKn: 'ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಕಿಸಾನ್‌ಕವಚ ಸಹಾಯಕ. ಸಾಲದ ಸ್ಥಿತಿ, ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು, ಬೆಳೆ ವಿಮೆ ಮತ್ತು ಸಂದೇಶಗಳ ಪರಿಶೀಲನೆಗೆ ನಾನು ಸಹಾಯ ಮಾಡುತ್ತೇನೆ.',
    suggestedActions: [
      { label: 'Check KCC Status', href: '/farmer/kcc' },
      { label: 'View Benefits', href: '/farmer/benefits' },
      { label: 'Verify SMS/Link', href: '/farmer/fraud' },
    ],
    isSandbox: true,
  };
}
