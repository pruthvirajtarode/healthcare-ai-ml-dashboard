# UML Diagrams for Healthcare AI/ML System

This folder contains professional UML diagrams documenting the Healthcare AI/ML Risk Analysis system architecture and design.

## 📊 Available Diagrams

### 1. **Use Case Diagram** (`use-case-diagram.svg`)
- **Purpose**: Shows system functionality from user perspective
- **Actors**: 
  - Healthcare Professional
  - System Admin
- **Key Use Cases**:
  - View Dashboard Overview
  - Analyze Patient Data
  - Predict Health Risks
  - View High-Risk Patients
  - Monitor KPIs
  - Generate Reports
  - Manage Patient Records
  - Configure System Settings
  - Export Data

### 2. **Class Diagram** (`class-diagram.svg`)
- **Purpose**: Defines the object-oriented structure of the system
- **Main Classes**:
  - **Patient**: Core data model with patient attributes and methods
  - **DataProcessor**: Data cleaning and validation logic
  - **RiskAnalyzer**: ML-based risk prediction engine
  - **Dashboard**: UI controller for visualization
  - **KPICalculator**: Healthcare metrics computation
- **Relationships**: Shows dependencies and interactions between classes

### 3. **Sequence Diagram** (`sequence-diagram.svg`)
- **Purpose**: Illustrates the risk prediction workflow step-by-step
- **Process Flow**:
  1. User clicks Predict Button
  2. Dashboard UI submits patient data
  3. Data Processor validates input
  4. Fetches patient history from database
  5. Sends processed data to ML Model
  6. ML Model runs prediction algorithm
  7. Returns risk score with 92.86% confidence
  8. Results displayed to user
- **Components**: User, Dashboard UI, Data Processor, ML Model, Database

### 4. **System Architecture** (`system-architecture.svg`)
- **Purpose**: Shows the complete system structure and technology stack
- **Layers**:
  - **Presentation Layer**: Web/Mobile browsers, Dashboard UI, Chart.js
  - **Application Layer**: Controllers, Data Management, Risk Analysis, KPI Calculator
  - **Data Layer**: Patient Database, ML Model Storage, Config Files, Logs
  - **External Services**: ML Training, Validation, Authentication

## 🖼️ Viewing the Diagrams

All diagrams are created in **SVG format** (Scalable Vector Graphics):
- **Advantages**: 
  - Perfect quality at any zoom level
  - Small file size
  - Can be edited directly in code
  - Viewable in any modern browser

### How to View:
1. **In Browser**: Double-click any `.svg` file to open in your default browser
2. **In VS Code**: Install "SVG Preview" extension
3. **In Documentation**: Embed directly in HTML/Markdown

## 📐 Technical Details

- **Format**: SVG (Scalable Vector Graphics)
- **Standard**: UML 2.0 notation
- **Color Coding**: 
  - Blue: Presentation/UI components
  - Green: Application logic
  - Orange: Data storage
  - Purple: External services
  - Teal: Healthcare professionals
  - Amber: Administrators

## 💡 Usage

These diagrams are ideal for:
- ✅ Project documentation
- ✅ Academic submissions
- ✅ Technical presentations
- ✅ System design discussions
- ✅ Developer onboarding
- ✅ Portfolio showcase

## 🔄 Converting to PNG (Optional)

If you need PNG format for presentations or documents:

**Method 1: Using Browser**
1. Open the SVG file in any browser
2. Right-click → "Save As" or "Export"
3. Choose PNG format

**Method 2: Using Online Tool**
- Visit: https://cloudconvert.com/svg-to-png
- Upload SVG files
- Download PNG versions

**Method 3: Using Command Line** (if you have Inkscape installed)
```bash
inkscape --export-type=png use-case-diagram.svg
inkscape --export-type=png class-diagram.svg
inkscape --export-type=png sequence-diagram.svg
inkscape --export-type=png system-architecture.svg
```

## 📄 License

Part of the Healthcare AI/ML Project
© 2026 Healthcare AI/ML Project

---

**Created with**: Professional SVG graphics and UML 2.0 standards  
**Last Updated**: February 2026
