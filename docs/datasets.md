# Dataset Documentation

## Overview

This directory contains datasets used for training and validating CarbonScope's AI models.

## Directory Structure

```
data/
├── datasets/
│   ├── materials/          # Material classification data
│   ├── products/           # Product information and carbon data
│   ├── supply_chain/       # Supply chain and shipping data
│   └── community/          # Community-contributed data
├── models/                 # Trained model files
├── processed/              # Processed and cleaned datasets
└── raw/                    # Raw data files
```

## Datasets

### 1. Material Classification Dataset
- **Purpose**: Train material detection models
- **Size**: ~50,000 images across 15 material categories
- **Format**: Images + JSON annotations
- **Source**: OpenImages, custom collection, community contributions

**Materials Covered**:
- Plastics (PET, HDPE, PVC, LDPE, PP, PS)
- Metals (Aluminum, Steel, Copper)
- Paper/Cardboard
- Glass
- Wood
- Textiles

### 2. Carbon Footprint Database
- **Purpose**: Carbon emission factors for materials and processes
- **Size**: ~10,000 entries
- **Format**: CSV with standardized units (kg CO2e)
- **Sources**: 
  - IPCC reports
  - Government environmental agencies
  - Academic research
  - Industry lifecycle assessments

**Columns**:
- material_type
- process_type
- carbon_intensity_kg_co2e_per_kg
- uncertainty_range
- source
- last_updated

### 3. Product Database
- **Purpose**: Product information and existing carbon data
- **Size**: ~100,000 products
- **Format**: JSON records
- **Sources**:
  - OpenFoodFacts
  - GS1 barcode database
  - Retailer APIs
  - Community contributions

**Fields**:
- barcode/gtin
- product_name
- brand
- category
- materials
- weight
- packaging_type
- carbon_footprint (if available)
- country_of_origin

### 4. Supply Chain Data
- **Purpose**: Shipping routes and transportation emissions
- **Size**: Global shipping network data
- **Format**: Graph database + CSV
- **Sources**:
  - Maritime shipping databases
  - Transportation emission factors
  - Port and logistics data

## Data Quality Standards

### Data Validation
- All datasets undergo automated validation
- Manual review for community contributions
- Source verification and citation requirements
- Regular updates and accuracy checks

### Privacy and Ethics
- No personal data collection
- Anonymized community contributions
- Open data principles where possible
- Respect for intellectual property

## Contributing Data

### Individual Contributors
1. Follow data format specifications
2. Provide source documentation
3. Include uncertainty estimates
4. Submit via GitHub or community portal

### Organizations
1. Partnership agreements available
2. Data sharing protocols established
3. Attribution and licensing terms
4. Bulk data ingestion pipelines

## Data Licensing

- **Open Datasets**: CC BY 4.0 (Attribution)
- **Community Data**: User grants usage rights
- **Commercial Data**: Specific licensing terms
- **Derived Works**: Maintain original licensing

## Quality Metrics

- **Completeness**: >95% for core fields
- **Accuracy**: Validated against multiple sources
- **Freshness**: Updated quarterly minimum
- **Coverage**: Global representation target

## API Access

Datasets are accessible via:
- REST API endpoints
- GraphQL queries
- Bulk download (registered users)
- Real-time streaming (partners)

## Research Applications

These datasets support:
- Academic research in sustainability
- Corporate carbon accounting
- Policy development and analysis
- Consumer awareness tools
- Environmental impact assessment

---

For questions about datasets, contact: data@carbonscope.org
