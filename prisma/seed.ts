import { PrismaClient, Role, ApplicationStage, ApplicationStatus, GrievanceCategory, GrievanceStatus, RiskLevel } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Starting KisanKavach Karnataka database seeding...');

  // Clear existing data safely
  await prisma.auditLog.deleteMany();
  await prisma.notification.deleteMany();
  await prisma.fraudReport.deleteMany();
  await prisma.grievanceComment.deleteMany();
  await prisma.grievance.deleteMany();
  await prisma.insuranceClaim.deleteMany();
  await prisma.insurancePolicy.deleteMany();
  await prisma.farmerBenefit.deleteMany();
  await prisma.benefitScheme.deleteMany();
  await prisma.kCCDocument.deleteMany();
  await prisma.kCCApplicationStatusHistory.deleteMany();
  await prisma.kCCApplication.deleteMany();
  await prisma.crop.deleteMany();
  await prisma.landHolding.deleteMany();
  await prisma.farmer.deleteMany();
  await prisma.user.deleteMany();
  await prisma.bankBranch.deleteMany();
  await prisma.bank.deleteMany();
  await prisma.village.deleteMany();
  await prisma.taluk.deleteMany();
  await prisma.district.deleteMany();
  await prisma.sLAConfiguration.deleteMany();

  const passwordHash = await bcrypt.hash('demo123', 10);

  // 1. Seed Districts
  const districtsData = [
    { code: 'MYS', name: 'Mysuru', nameKn: 'ಮೈಸೂರು' },
    { code: 'BLR', name: 'Bengaluru Rural', nameKn: 'ಬೆಂಗಳೂರು ಗ್ರಾಮಾಂತರ' },
    { code: 'MND', name: 'Mandya', nameKn: 'ಮಂಡ್ಯ' },
    { code: 'TUM', name: 'Tumakuru', nameKn: 'ತುಮಕೂರು' },
    { code: 'BEL', name: 'Belagavi', nameKn: 'ಬೆಳಗಾವಿ' },
    { code: 'DHW', name: 'Dharwad', nameKn: 'ಧಾರವಾಡ' },
    { code: 'VJP', name: 'Vijayapura', nameKn: 'ವಿಜಯಪುರ' },
    { code: 'RCH', name: 'Raichur', nameKn: 'ರಾಯಚೂರು' },
    { code: 'KLB', name: 'Kalaburagi', nameKn: 'ಕಲಬುರಗಿ' },
    { code: 'SHM', name: 'Shivamogga', nameKn: 'ಶಿವಮೊಗ್ಗ' },
  ];

  const districtMap = new Map<string, string>();
  for (const d of districtsData) {
    const created = await prisma.district.create({ data: d });
    districtMap.set(d.code, created.id);
  }

  const mysuruId = districtMap.get('MYS')!;
  const mandyaId = districtMap.get('MND')!;

  // 2. Seed Taluks & Villages for Mysuru & Mandya
  const talukMysuru = await prisma.taluk.create({
    data: { code: 'NJG', name: 'Nanjangud', nameKn: 'ನಂಜನಗೂಡು', districtId: mysuruId },
  });
  const talukMandya = await prisma.taluk.create({
    data: { code: 'MND_T', name: 'Mandya Taluk', nameKn: 'ಮಂಡ್ಯ ತಾಲೂಕು', districtId: mandyaId },
  });

  const villageHullahalli = await prisma.village.create({
    data: { code: 'HUL', name: 'Hullahalli', nameKn: 'ಹುಲ್ಲಹಳ್ಳಿ', talukId: talukMysuru.id },
  });
  const villageMaddur = await prisma.village.create({
    data: { code: 'MDR', name: 'Maddur Village', nameKn: 'ಮದ್ದೂರು ಗ್ರಾಮ', talukId: talukMandya.id },
  });

  // 3. Seed Banks & Branches
  const banksData = [
    { code: 'KBL', name: 'Karnataka Bank', type: 'Private Commercial' },
    { code: 'KVGB', name: 'Karnataka Vikas Grameena Bank', type: 'RRB' },
    { code: 'PKGB', name: 'Pragathi Krishna Gramin Bank', type: 'RRB' },
    { code: 'KSCAB', name: 'Karnataka State Cooperative Apex Bank', type: 'Cooperative' },
    { code: 'CNRB', name: 'Canara Bank', type: 'Public Sector Bank' },
    { code: 'SBIN', name: 'State Bank of India', type: 'Public Sector Bank' },
  ];

  const bankMap = new Map<string, string>();
  for (const b of banksData) {
    const created = await prisma.bank.create({ data: b });
    bankMap.set(b.code, created.id);
  }

  const branchMysuruMain = await prisma.bankBranch.create({
    data: {
      bankId: bankMap.get('KBL')!,
      branchName: 'Nanjangud Main Branch',
      ifscCode: 'KARB0000412',
      districtId: mysuruId,
      talukId: talukMysuru.id,
    },
  });

  const branchCanaraMandya = await prisma.bankBranch.create({
    data: {
      bankId: bankMap.get('CNRB')!,
      branchName: 'Mandya Market Branch',
      ifscCode: 'CNRB0001890',
      districtId: mandyaId,
      talukId: talukMandya.id,
    },
  });

  // Additional Branches across districts
  const additionalBranches = [];
  const districtIds = Array.from(districtMap.values());
  const bankIds = Array.from(bankMap.values());

  for (let i = 0; i < 20; i++) {
    const distId = districtIds[i % districtIds.length];
    const bId = bankIds[i % bankIds.length];
    const br = await prisma.bankBranch.create({
      data: {
        bankId: bId,
        branchName: `Branch #${101 + i}`,
        ifscCode: `KVK${1000 + i}`,
        districtId: distId,
        talukId: talukMysuru.id,
      },
    });
    additionalBranches.push(br);
  }

  const allBranches = [branchMysuruMain, branchCanaraMandya, ...additionalBranches];

  // 4. Seed Demo Users & Primary Farmer
  const userAdmin = await prisma.user.create({
    data: {
      email: 'admin@demo.kisankavach.in',
      passwordHash,
      name: 'System Administrator',
      role: Role.ADMIN,
      mobile: '9876543210',
    },
  });

  const userGov = await prisma.user.create({
    data: {
      email: 'gov@demo.kisankavach.in',
      passwordHash,
      name: 'Dr. Vijayalakshmi (State Agri Commissioner)',
      role: Role.GOVT_OFFICER,
      mobile: '9876543211',
    },
  });

  const userDistrict = await prisma.user.create({
    data: {
      email: 'district@demo.kisankavach.in',
      passwordHash,
      name: 'Anand Rao (District Collector Mysuru)',
      role: Role.DISTRICT_OFFICER,
      mobile: '9876543212',
      districtId: mysuruId,
    },
  });

  const userBank = await prisma.user.create({
    data: {
      email: 'bank@demo.kisankavach.in',
      passwordHash,
      name: 'Suresh Kumar (Nanjangud Branch Manager)',
      role: Role.BANK_OFFICER,
      mobile: '9876543213',
      bankBranchId: branchMysuruMain.id,
    },
  });

  const userFarmerPrimary = await prisma.user.create({
    data: {
      email: 'farmer@demo.kisankavach.in',
      passwordHash,
      name: 'Ramesh Gowda',
      role: Role.FARMER,
      mobile: '9845012345',
    },
  });

  const farmerPrimary = await prisma.farmer.create({
    data: {
      farmerIdCode: 'KK-KA-100245',
      userId: userFarmerPrimary.id,
      name: 'Ramesh Gowda',
      nameKn: 'ರಮೇಶ್‌ ಗೌಡ',
      mobile: '9845012345',
      aadhaarMasked: 'XXXX-XXXX-4821',
      villageId: villageHullahalli.id,
      talukId: talukMysuru.id,
      districtId: mysuruId,
      landSizeAcres: 3.5,
      verificationStatus: 'VERIFIED',
      fruitsId: 'FRUITS-MYS-8821',
      bhoomiId: 'BHOOMI-RTC-142-1A',
    },
  });

  // Seed Landholding & Crops for primary farmer
  const lh1 = await prisma.landHolding.create({
    data: {
      farmerId: farmerPrimary.id,
      surveyNumberMasked: '142/1A',
      villageName: 'Hullahalli',
      areaAcres: 2.0,
      soilType: 'Red Loamy',
      irrigationStatus: 'Rainfed',
      fruitsRef: 'FRUITS-LAND-142',
      bhoomiRef: 'BHOOMI-RTC-142-1A',
    },
  });

  await prisma.crop.create({
    data: {
      landHoldingId: lh1.id,
      cropName: 'Ragi (Finger Millet)',
      cropNameKn: 'ರಾಗಿ',
      season: 'Kharif',
      areaAcres: 2.0,
      expectedYield: '24 Quintals',
    },
  });

  const lh2 = await prisma.landHolding.create({
    data: {
      farmerId: farmerPrimary.id,
      surveyNumberMasked: '142/2B',
      villageName: 'Hullahalli',
      areaAcres: 1.5,
      soilType: 'Black Cotton',
      irrigationStatus: 'Canal Irrigated',
      fruitsRef: 'FRUITS-LAND-143',
      bhoomiRef: 'BHOOMI-RTC-142-2B',
    },
  });

  await prisma.crop.create({
    data: {
      landHoldingId: lh2.id,
      cropName: 'Paddy (Rice)',
      cropNameKn: 'ಭತ್ತ',
      season: 'Kharif',
      areaAcres: 1.5,
      expectedYield: '30 Quintals',
    },
  });

  // 5. Seed 100+ Realistic Mock Farmers
  console.log('👨‍🌾 Seeding 100+ Farmers...');
  const firstNames = ['Siddaramaiah', 'Basavaraj', 'Kumaraswamy', 'Devegowda', 'Shivakumar', 'Yediyurappa', 'Mallikarjun', 'Nitin', 'Manjunath', 'Lokesh', 'Prakash', 'Mahesh', 'Ganesh', 'Venkat', 'Suresh', 'Ramesh', 'Shantha', 'Lakshmi', 'Parvathi', 'Anusuya'];
  const lastNames = ['Gowda', 'Patil', 'Shetty', 'Nayak', 'Hegde', 'Kulkarni', 'Bhat', 'Rao', 'Reddy', 'Pujari', 'Joshi', 'Chavan'];

  const farmerList = [farmerPrimary];

  for (let i = 1; i <= 105; i++) {
    const fn = firstNames[i % firstNames.length];
    const ln = lastNames[i % lastNames.length];
    const fullName = `${fn} ${ln}`;
    const email = `farmer${i}@demo.kisankavach.in`;
    const distId = districtIds[i % districtIds.length];

    const user = await prisma.user.create({
      data: {
        email,
        passwordHash,
        name: fullName,
        role: Role.FARMER,
        mobile: `9845${100000 + i}`,
      },
    });

    const f = await prisma.farmer.create({
      data: {
        farmerIdCode: `KK-KA-${100000 + i}`,
        userId: user.id,
        name: fullName,
        nameKn: `${fn} ${ln}`,
        mobile: `9845${100000 + i}`,
        aadhaarMasked: `XXXX-XXXX-${3000 + i}`,
        villageId: i % 2 === 0 ? villageHullahalli.id : villageMaddur.id,
        talukId: i % 2 === 0 ? talukMysuru.id : talukMandya.id,
        districtId: distId,
        landSizeAcres: Math.round((1.5 + (i % 8) * 0.75) * 10) / 10,
        verificationStatus: 'VERIFIED',
        fruitsId: `FRUITS-KA-${7000 + i}`,
        bhoomiId: `BHOOMI-RTC-${8000 + i}`,
      },
    });

    // Create landholding & crops for each farmer
    const lh = await prisma.landHolding.create({
      data: {
        farmerId: f.id,
        surveyNumberMasked: `${100 + i}/${(i % 5) + 1}A`,
        villageName: i % 2 === 0 ? 'Hullahalli' : 'Maddur',
        areaAcres: f.landSizeAcres,
        soilType: i % 2 === 0 ? 'Red Loamy' : 'Black Cotton',
        irrigationStatus: i % 3 === 0 ? 'Canal Irrigated' : 'Rainfed',
      },
    });

    await prisma.crop.create({
      data: {
        landHoldingId: lh.id,
        cropName: i % 2 === 0 ? 'Ragi' : i % 3 === 0 ? 'Sugarcane' : 'Maize',
        cropNameKn: i % 2 === 0 ? 'ರಾಗಿ' : i % 3 === 0 ? 'ಕಬ್ಬು' : 'ಮೆಕ್ಕೆಜೋಳ',
        season: 'Kharif',
        areaAcres: f.landSizeAcres,
        expectedYield: `${Math.round(f.landSizeAcres * 12)} Quintals`,
      },
    });

    farmerList.push(f);
  }

  // 6. Seed Benefit Schemes & Farmer Benefits
  console.log('🎁 Seeding Benefit Schemes...');
  const schemesData = [
    { code: 'PM-KISAN', name: 'PM-KISAN Samman Nidhi', nameKn: 'ಪಿಎಂ-ಕಿಸಾನ್ ಸಮ್ಮಾನ್ ನಿಧಿ', description: '₹6,000 annual direct income support to farmer families', provider: 'Central Govt', category: 'Income Support' },
    { code: 'PMFBY', name: 'Pradhan Mantri Fasal Bima Yojana', nameKn: 'ಪ್ರಧಾನ್ ಮಂತ್ರಿ ಫಸಲ್ ಭೀಮಾ ಯೋಜನೆ', description: 'Comprehensive crop insurance against natural calamities', provider: 'Central & State', category: 'Crop Insurance' },
    { code: 'KCC-SUB', name: 'KCC Interest Subvention Scheme', nameKn: 'ಕೆ.ಸಿ.ಸಿ ಬಡ್ಡಿ ರಿಯಾಯಿತಿ ಯೋಜನೆ', description: '3% prompt repayment interest subvention on short term crop loan', provider: 'NABARD / Bank', category: 'Credit Subvention' },
    { code: 'KRISHI-BHAGYA', name: 'Krishi Bhagya Subsidy', nameKn: 'ಕೃಷಿ ಭಾಗ್ಯ ಯೋಜನೆ', description: 'Subsidy for farm ponds, diesel pumpsets and shade nets', provider: 'Govt of Karnataka', category: 'Infrastructure Subsidy' },
    { code: 'MSP-PROC', name: 'Karnataka MSP Grain Procurement', nameKn: 'ಬೆಂಬಲ ಬೆಲೆ ಧಾನ್ಯ ಖರೀದಿ', description: 'Minimum Support Price procurement for Ragi, Jowar & Paddy', provider: 'KA Food & Civil Supplies', category: 'Procurement' },
  ];

  const schemeMap = new Map<string, string>();
  for (const s of schemesData) {
    const created = await prisma.benefitScheme.create({ data: s });
    schemeMap.set(s.code, created.id);
  }

  for (const f of farmerList) {
    await prisma.farmerBenefit.create({
      data: {
        farmerId: f.id,
        schemeId: schemeMap.get('PM-KISAN')!,
        status: 'Active',
        lastDisbursementDate: new Date('2026-01-15'),
        amountReceived: 2000,
        nextAction: 'Next installment due April 2026',
      },
    });

    await prisma.farmerBenefit.create({
      data: {
        farmerId: f.id,
        schemeId: schemeMap.get('PMFBY')!,
        status: 'Active',
        lastDisbursementDate: new Date('2025-11-20'),
        amountReceived: 0,
        nextAction: 'Policy Active for Kharif 2026',
      },
    });

    if (Math.random() > 0.4) {
      await prisma.farmerBenefit.create({
        data: {
          farmerId: f.id,
          schemeId: schemeMap.get('KCC-SUB')!,
          status: 'Eligible',
          nextAction: '3% interest subvention automatically applied upon prompt repayment',
        },
      });
    }
  }

  // 7. Seed 250+ KCC Applications
  console.log('💳 Seeding 250+ KCC Applications & Statuses...');
  const stages: ApplicationStage[] = [
    ApplicationStage.SUBMITTED,
    ApplicationStage.FARMER_VERIFICATION,
    ApplicationStage.LAND_VERIFICATION,
    ApplicationStage.DOCUMENT_VERIFICATION,
    ApplicationStage.CREDIT_ASSESSMENT,
    ApplicationStage.SANCTION_PENDING,
    ApplicationStage.SANCTIONED,
    ApplicationStage.DISBURSED,
    ApplicationStage.CLARIFICATION_REQUIRED,
    ApplicationStage.REJECTED,
  ];

  const rejectionReasons = [
    'Incomplete documentation (Bhoomi RTC mismatch)',
    'Eligibility issue (Existing defaulted loan at another bank)',
    'Credit assessment issue (Land area insufficient for requested amount)',
    'Duplicate application detected',
  ];

  for (let i = 1; i <= 255; i++) {
    const farmer = farmerList[i % farmerList.length];
    const branch = allBranches[i % allBranches.length];

    // Determine realistic distribution
    let stage: ApplicationStage = ApplicationStage.CREDIT_ASSESSMENT;
    let status: ApplicationStatus = ApplicationStatus.PROCESSING;
    let slaDaysElapsed = (i % 7);
    let slaBreached = false;
    let rejectionReason: string | undefined;

    if (i % 10 === 0) {
      // SLA Breached (10%)
      stage = ApplicationStage.CREDIT_ASSESSMENT;
      status = ApplicationStatus.SLA_BREACHED;
      slaDaysElapsed = 9; // > 7 allowed
      slaBreached = true;
    } else if (i % 15 === 0) {
      // Rejected (6-7%)
      stage = ApplicationStage.REJECTED;
      status = ApplicationStatus.REJECTED;
      rejectionReason = rejectionReasons[i % rejectionReasons.length];
    } else if (i % 12 === 0) {
      // Clarification required
      stage = ApplicationStage.CLARIFICATION_REQUIRED;
      status = ApplicationStatus.ACTION_REQUIRED;
    } else if (i % 3 === 0) {
      // Sanctioned / Disbursed (30%)
      stage = i % 2 === 0 ? ApplicationStage.SANCTIONED : ApplicationStage.DISBURSED;
      status = ApplicationStatus.SANCTIONED;
      slaDaysElapsed = 5;
    } else {
      // Normal stages
      stage = stages[i % 6];
      status = ApplicationStatus.PROCESSING;
    }

    const loanRequested = 50000 + (i % 15) * 10000;

    const createdApp = await prisma.kCCApplication.create({
      data: {
        applicationId: `KK-KA-2026-${100000 + i}`,
        farmerId: farmer.id,
        bankBranchId: branch.id,
        loanAmountRequested: loanRequested,
        loanAmountSanctioned: (stage === ApplicationStage.SANCTIONED || stage === ApplicationStage.DISBURSED) ? loanRequested : null,
        purpose: i % 2 === 0 ? 'Crop Cultivation & Input Costs (Ragi/Paddy)' : 'Agricultural Equipment & Micro-Irrigation',
        currentStage: stage,
        status: status,
        responsibleParty: `${branch.branchName}`,
        slaDaysTotal: 7,
        slaDaysElapsed: slaDaysElapsed,
        slaBreached: slaBreached,
        rejectionReason: rejectionReason || null,
        remarks: rejectionReason ? `Rejected during verification: ${rejectionReason}` : `Processing under standard SLA workflow.`,
        submittedAt: new Date(Date.now() - slaDaysElapsed * 24 * 60 * 60 * 1000),
      },
    });

    // Create documents for app
    await prisma.kCCDocument.createMany({
      data: [
        { applicationId: createdApp.id, docType: 'Aadhaar Card', docName: 'aadhaar_masked.pdf', fileUrl: '/docs/mock_aadhaar.pdf', verified: true },
        { applicationId: createdApp.id, docType: 'Bhoomi RTC Pahani', docName: 'bhoomi_rtc_142.pdf', fileUrl: '/docs/mock_rtc.pdf', verified: true },
        { applicationId: createdApp.id, docType: 'Bank Passbook', docName: 'bank_passbook.pdf', fileUrl: '/docs/mock_passbook.pdf', verified: true },
      ],
    });

    // Create history entries
    await prisma.kCCApplicationStatusHistory.create({
      data: {
        applicationId: createdApp.id,
        stage: ApplicationStage.SUBMITTED,
        status: ApplicationStatus.PROCESSING,
        actionByUser: farmer.name,
        remarks: 'Application submitted successfully via KisanKavach portal.',
        createdAt: new Date(Date.now() - slaDaysElapsed * 24 * 60 * 60 * 1000),
      },
    });
  }

  // Primary Farmer Application
  const primaryApp = await prisma.kCCApplication.create({
    data: {
      applicationId: 'KK-KA-2026-000123',
      farmerId: farmerPrimary.id,
      bankBranchId: branchMysuruMain.id,
      loanAmountRequested: 120000,
      loanAmountSanctioned: null,
      purpose: 'Kharif Ragi & Paddy Crop Cultivation Loan',
      currentStage: ApplicationStage.CREDIT_ASSESSMENT,
      status: ApplicationStatus.PROCESSING,
      responsibleParty: `${branchMysuruMain.branchName}`,
      slaDaysTotal: 7,
      slaDaysElapsed: 3,
      slaBreached: false,
      remarks: 'Land records verified with Bhoomi API sandbox. Under credit risk review by branch manager.',
      submittedAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
    },
  });

  await prisma.kCCDocument.createMany({
    data: [
      { applicationId: primaryApp.id, docType: 'Aadhaar Card', docName: 'aadhaar_ramesh.pdf', fileUrl: '/docs/mock_aadhaar.pdf', verified: true },
      { applicationId: primaryApp.id, docType: 'Bhoomi RTC Pahani', docName: 'bhoomi_rtc_hullahalli.pdf', fileUrl: '/docs/mock_rtc.pdf', verified: true },
      { applicationId: primaryApp.id, docType: 'Soil Health Card', docName: 'soil_health_report.pdf', fileUrl: '/docs/mock_soil.pdf', verified: true },
    ],
  });

  // 8. Seed Insurance Policies
  console.log('🛡️ Seeding Insurance Policies...');
  for (let i = 1; i <= 105; i++) {
    const f = farmerList[i % farmerList.length];
    await prisma.insurancePolicy.create({
      data: {
        policyNumber: `KK-INS-2026-${100000 + i}`,
        farmerId: f.id,
        crop: i % 2 === 0 ? 'Ragi' : 'Paddy',
        season: 'Kharif',
        year: 2026,
        sumInsured: 45000,
        premiumPaid: 900,
        policyStatus: 'Active',
        claimStatus: i % 8 === 0 ? 'Claim Under Assessment' : 'No Active Claim',
      },
    });
  }

  // 9. Seed 50+ Grievances
  console.log('📢 Seeding 50+ Grievances...');
  const grievanceCategories: GrievanceCategory[] = [
    GrievanceCategory.KCC,
    GrievanceCategory.BANK,
    GrievanceCategory.INSURANCE,
    GrievanceCategory.GOVT_BENEFIT,
    GrievanceCategory.SUBSIDY,
    GrievanceCategory.FRAUD,
  ];

  const grievanceSubjects = [
    'Delay in KCC loan credit assessment past 7 days',
    'Bank branch requesting physical documents already verified online',
    'PMFBY Crop Insurance premium debited but policy confirmation pending',
    'PM-KISAN 16th installment not credited to bank account',
    'Suspected fake call received claiming to be KCC sanction officer',
  ];

  for (let i = 1; i <= 52; i++) {
    const f = farmerList[i % farmerList.length];
    const cat = grievanceCategories[i % grievanceCategories.length];
    const subj = grievanceSubjects[i % grievanceSubjects.length];

    await prisma.grievance.create({
      data: {
        grievanceId: `KK-GR-2026-${100000 + i}`,
        farmerId: f.id,
        applicationId: primaryApp.id,
        category: cat,
        subject: subj,
        description: `${subj}. Farmer requested urgent intervention from District Agricultural Officer.`,
        status: i % 3 === 0 ? GrievanceStatus.RESOLVED : GrievanceStatus.UNDER_REVIEW,
        priority: i % 5 === 0 ? 'HIGH' : 'MEDIUM',
        assignedToUserId: userDistrict.id,
      },
    });
  }

  // Primary Farmer Grievance
  await prisma.grievance.create({
    data: {
      grievanceId: 'KK-GR-2026-000045',
      farmerId: farmerPrimary.id,
      applicationId: primaryApp.id,
      category: GrievanceCategory.KCC,
      subject: 'Clarification regarding land survey number verification timing',
      description: 'Submitted application 3 days ago. Requesting branch officer to expedite Bhoomi RTC verification.',
      status: GrievanceStatus.UNDER_REVIEW,
      priority: 'MEDIUM',
      assignedToUserId: userDistrict.id,
    },
  });

  // 10. Seed 30+ Fraud Reports
  console.log('🚨 Seeding 30+ Fraud Reports...');
  const fraudTexts = [
    'Urgent! Your KCC loan of Rs. 1,50,000 is approved. Click bit.ly/kcc-claim-now to pay processing fee.',
    'Your PM-KISAN account is suspended due to KYC. Share OTP immediately with Bank Executive.',
    'Government is offering 90% subsidy on tractor. Pay Rs 2000 registration fee to UPI ID agri-gov@upi.',
    'Dear farmer, your crop insurance claim of Rs 45,000 is ready. Call 9811223344 with your PIN.',
  ];

  for (let i = 1; i <= 32; i++) {
    const text = fraudTexts[i % fraudTexts.length];
    await prisma.fraudReport.create({
      data: {
        reportId: `KK-FR-2026-${10000 + i}`,
        farmerId: farmerList[i % farmerList.length].id,
        category: i % 2 === 0 ? 'Fake KCC Approval Scam' : 'PM-KISAN Phishing SMS',
        textAnalyzed: text,
        source: i % 2 === 0 ? 'SMS' : 'WhatsApp',
        riskScore: 85 + (i % 12),
        riskLevel: RiskLevel.HIGH,
        reportedToGovt: true,
      },
    });
  }

  // 11. Seed SLA Configuration & Initial Audit Log
  const defaultSLARules = [
    { stage: ApplicationStage.SUBMITTED, workingDaysAllowed: 1 },
    { stage: ApplicationStage.FARMER_VERIFICATION, workingDaysAllowed: 2 },
    { stage: ApplicationStage.LAND_VERIFICATION, workingDaysAllowed: 2 },
    { stage: ApplicationStage.DOCUMENT_VERIFICATION, workingDaysAllowed: 2 },
    { stage: ApplicationStage.CREDIT_ASSESSMENT, workingDaysAllowed: 5 },
    { stage: ApplicationStage.SANCTION_PENDING, workingDaysAllowed: 3 },
  ];

  for (const rule of defaultSLARules) {
    await prisma.sLAConfiguration.create({ data: rule });
  }

  await prisma.auditLog.create({
    data: {
      userId: userAdmin.id,
      userRole: 'ADMIN',
      action: 'DATABASE_INITIALIZED',
      entity: 'System',
      entityId: 'SYSTEM-001',
      metadataJson: JSON.stringify({ message: 'KisanKavach Karnataka database seeded with pilot sandbox data.' }),
      ipAddress: '127.0.0.1',
    },
  });

  console.log('✅ KisanKavach Karnataka Seeding Completed Successfully!');
}

main()
  .catch((e) => {
    console.error('❌ Seeding failed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
