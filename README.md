# Propeller Fault Prediction Model using SVM RBF Kernel

## Project Overview
This repository contains a Data Science project focused on predicting faults in wind turbine propeller blades using Support Vector Machine (SVM) with an RBF Kernel. The project leverages vibration signal data to classify common propeller faults such as surface erosion, cracking, mass imbalance, and pitch angle deformation. It was developed as part of the "Mathematics for Artificial Intelligence" course at the University of Technology and Education, Ho Chi Minh City.

## Repository Details
- **GitHub Link**: [https://github.com/HueyAnthonyDisward/Propeller-Fault-Prediction-Model-using-SVM-RBF](https://github.com/HueyAnthonyDisward/Propeller-Fault-Prediction-Model-using-SVM-RBF)
- **Language/Tools**: Python, scikit-learn, pandas, matplotlib, Jupyter Notebook
- **Dataset**: Vibration signals from Ogaili et al. (2023), collected at the Renewable Energy Lab, University of Mustansiriyah, Baghdad, Iraq
- **Purpose**: Build an automated fault classification system to enhance wind turbine maintenance and operational efficiency.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Required libraries: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `jupyter`
- Access to the vibration dataset (e.g., `merged_wind_turbine_data.csv`)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/HueyAnthonyDisward/Propeller-Fault-Prediction-Model-using-SVM-RBF.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Propeller-Fault-Prediction-Model-using-SVM-RBF
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Ensure the dataset file (`merged_wind_turbine_data.csv`) and other files are in the root directory.

### Usage
- Run the Jupyter Notebook for an interactive exploration:
  ```bash
  jupyter notebook Test.ipynb
  ```
- Execute `gopfile.py` to run additional processing or analysis:
  ```bash
  python gopfile.py
  ```
- Use the optimized models (`wind_turbine_pca_optimized_v5.pkl`, `wind_turbine_svm_rbf_model_optimized_v5.pkl`, `wind_turbine_svm_scaler_optimized_v5.pkl`) for predictions or further development by loading them in your Python environment.

## Project Structure
- `Vibration dataset vs. wind speed/`: Directory containing vibration dataset details.
- `FinalReport_NhomNguyenTrungHieu_22110138.pdf`: Project report detailing methodology and results.
- `Test.ipynb`: Jupyter Notebook for interactive analysis and testing.
- `gopfile.py`: Python script for additional processing.
- `merged_wind_turbine_data.csv`: Merged dataset of vibration signals.
- `wind_turbine_pca_optimized_v5.pkl`: Optimized PCA model file.
- `wind_turbine_svm_rbf_model_optimized_v5.pkl`: Optimized SVM RBF model file.
- `wind_turbine_svm_scaler_optimized_v5.pkl`: Optimized scaler file for preprocessing.
- `README.md`: This file.

## Methodology
The project uses SVM with an RBF Kernel to classify propeller faults based on vibration signals. Key steps include:
1. **Data Preprocessing**: Extract features from `merged_wind_turbine_data.csv` and apply PCA optimization.
2. **Model Training**: Train an SVM model with RBF Kernel, optimizing parameters using cross-validation.
3. **Evaluation**: Assess model performance using accuracy and other metrics.

The dataset includes vibration signals collected at wind speeds from 1.3 m/s to 5.6 m/s, covering healthy and faulty states.

## Results
- The optimized SVM model demonstrates improved performance on the processed dataset.
- Detailed results are available in the report: `FinalReport_NhomNguyenTrungHieu_22110138.pdf`.

## Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- **Instructor**: Dr. Bùi Mạnh Quân
- **Team Members**: Nguyễn Trung Hiếu (22110138), Lê Hoàng Bảo Phúc (22110200), Phạm Anh Quân (22110215)
- **Data Source**: Ogaili et al. (2023), published in *Data in Brief*
- **Institution**: University of Technology and Education, Ho Chi Minh City


##Result:
![image](https://github.com/user-attachments/assets/8855c550-fa2a-4da4-bcb6-afaed7642a55)

