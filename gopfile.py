import pandas as pd
import os
import re

# Đường dẫn chính xác đến thư mục chứa file dữ liệu
base_path = r"Vibration dataset vs. wind speed"
subfolder = "Vibration dataset vs. wind speed"
folder_path = os.path.join(base_path, subfolder) if os.path.exists(os.path.join(base_path, subfolder)) else base_path

# Lấy thư mục chứa file Python (gopfile.py)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Lấy danh sách file từ thư mục dữ liệu
files = [f for f in os.listdir(folder_path) if f.endswith(('.csv', '.xlsx'))]
if not files:
    print(f"Không tìm thấy file CSV/XLSX nào trong thư mục: {folder_path}")
    exit(1)

# Gán nhãn và lưu thông tin file
file_label_map = {}
for file in files:
    file_lower = file.lower()
    if "h-" in file_lower or "h for" in file_lower:
        label = 0  # Healthy
    elif "erosion" in file_lower:
        label = 1  # Surface Erosion
    elif "crack" in file_lower:
        label = 2  # Cracked Blade
    elif "unbalance" in file_lower or "unbalnce" in file_lower:  # Sửa lỗi chính tả
        label = 3  # Mass Imbalance
    elif "twist" in file_lower or "twsist" in file_lower:
        label = 4  # Twist Blade Fault
    else:
        label = -1  # Nhãn không xác định
    file_label_map[file] = label

# Kiểm tra phân bố nhãn
label_counts = pd.Series(file_label_map.values()).value_counts()
label_names = ["Healthy", "Surface Erosion", "Cracked Blade", "Mass Imbalance", "Twist Blade Fault"]
print("Phân bố nhãn:")
for label in sorted(label_counts.keys()):
    if label == -1:
        print(f"Không xác định: {label_counts[label]} file")
    else:
        print(f"{label_names[label]}: {label_counts[label]} file")

# In danh sách file với label = -1
unknown_files = [file for file, label in file_label_map.items() if label == -1]
if unknown_files:
    print("\nCác file không xác định (label = -1):")
    for file in unknown_files:
        print(file)

# Đọc và gộp dữ liệu
data = []
for file, label in file_label_map.items():
    file_path = os.path.join(folder_path, file)
    if not os.path.exists(file_path):
        print(f"File không tồn tại: {file_path}")
        continue

    print(f"Đang xử lý file: {file}")
    # Đọc file
    try:
        if file.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            print(f"Không hỗ trợ định dạng file: {file}")
            continue
    except Exception as e:
        print(f"Lỗi khi đọc file {file}: {e}")
        continue

    # Chuẩn hóa dữ liệu
    # Kiểm tra các cột trong file
    columns = df.columns.tolist()
    print(f"Các cột trong file {file}: {columns}")  # Thêm dòng này để kiểm tra cột

    if "Time - Voltage_1" in df.columns and "Amplitude - Voltage_1" in df.columns:
        # File .xlsx có cột riêng lẻ (như twist.xlsx)
        df = df.rename(columns={"Time - Voltage_1": "time", "Amplitude - Voltage_1": "amplitude"})
        df["amplitude"] = df["amplitude"].astype(float) * 10  # Chuyển từ Voltage sang g
    elif "Time - sec" in df.columns and "Amplitude - g" in df.columns:
        # File .csv có cột riêng lẻ
        df = df.rename(columns={"Time - sec": "time", "Amplitude - g": "amplitude"})
        df["amplitude"] = df["amplitude"].astype(float)  # Đã ở đơn vị g
    elif "Time - Voltage_1;Amplitude - Voltage_1" in df.columns:
        # File có cột ghép (dạng chuỗi)
        time_amp = df["Time - Voltage_1;Amplitude - Voltage_1"].str.split(";", expand=True)
        time_amp = time_amp.dropna()  # Loại bỏ dòng có giá trị NaN
        time_amp = time_amp[time_amp[0].str.strip() != ""]  # Loại bỏ dòng có time rỗng
        time_amp = time_amp[time_amp[1].str.strip() != ""]  # Loại bỏ dòng có amplitude rỗng
        if time_amp.empty:
            print(f"File {file} không có dữ liệu hợp lệ sau khi lọc.")
            continue
        try:
            df = df.loc[time_amp.index]  # Chỉ giữ các dòng hợp lệ
            df["time"] = time_amp[0].astype(float)
            df["amplitude"] = time_amp[1].astype(float) * 10  # Chuyển từ Voltage sang g
        except Exception as e:
            print(f"Lỗi khi chuẩn hóa dữ liệu trong file {file}: {e}")
            continue
    elif "Time - sec;Amplitude - g" in df.columns:
        # File có cột ghép (dạng chuỗi)
        time_amp = df["Time - sec;Amplitude - g"].str.split(";", expand=True)
        time_amp = time_amp.dropna()
        time_amp = time_amp[time_amp[0].str.strip() != ""]
        time_amp = time_amp[time_amp[1].str.strip() != ""]
        if time_amp.empty:
            print(f"File {file} không có dữ liệu hợp lệ sau khi lọc.")
            continue
        try:
            df = df.loc[time_amp.index]
            df["time"] = time_amp[0].astype(float)
            df["amplitude"] = time_amp[1].astype(float)  # Đã ở đơn vị g
        except Exception as e:
            print(f"Lỗi khi chuẩn hóa dữ liệu trong file {file}: {e}")
            continue
    else:
        print(f"File {file} không có cột dữ liệu phù hợp (Time và Amplitude).")
        continue




    # Gán nhãn
    df["label"] = label

    # Trích xuất tốc độ gió
    match = re.search(r"vw(ind)?=([\d\.]+)", file.lower())
    if match:
        wind_speed_str = match.group(2).rstrip('.')
        try:
            wind_speed = float(wind_speed_str)
        except ValueError:
            print(f"Không thể chuyển đổi tốc độ gió từ file {file}: {wind_speed_str}")
            wind_speed = 0.0
    else:
        print(f"Không tìm thấy tốc độ gió trong file {file}")
        wind_speed = 0.0
    df["wind_speed"] = wind_speed

    # Chỉ giữ các cột cần thiết
    df = df[["time", "amplitude", "label", "wind_speed"]]
    data.append(df)

# Gộp thành một DataFrame
if data:
    merged_data = pd.concat(data, ignore_index=True)

    # Kiểm tra dữ liệu gộp
    print("\nThông tin dữ liệu gộp:")
    print(merged_data.info())
    print("\nMẫu dữ liệu đầu tiên:")
    print(merged_data.head())

    # Lưu dữ liệu gộp trong cùng thư mục với file Python
    output_path = os.path.join(script_dir, "merged_wind_turbine_data.csv")
    merged_data.to_csv(output_path, index=False)
    print(f"\nĐã lưu dữ liệu gộp vào '{output_path}'")
else:
    print("Không có dữ liệu nào được đọc. Vui lòng kiểm tra lại các file.")