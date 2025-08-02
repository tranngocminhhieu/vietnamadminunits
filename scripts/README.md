# Scripts Overview

This directory contains utility scripts used throughout the project. Each subfolder is responsible for a specific stage in the data pipeline.

## 📥 [`collecting_data`](collecting_data)
Scripts for scraping and collecting administrative unit data from multiple sources.

## 🧹 [`processing_data`](processing_data)
Cleans, merges, and enriches raw data into multiple useful datasets.  
Results can be found in the [`data/processed`](../data/processed) directory.

## 🧱 [`generating_module_data`](generating_module_data)
Generates structured data used by the core library [`vietnamadminunits`](../vietnamadminunits).  
Results can be found in the [`vietnamadminunits/data`](../vietnamadminunits/data) directory.

## 🧪 [`module_testing`](module_testing)
Scripts for testing and validating the [`vietnamadminunits`](../vietnamadminunits) module's functionality.