"""Convert CSV data to Parquet format for faster loading."""
import pandas as pd
from pathlib import Path

def convert_to_parquet():
    """Convert tr_cre.csv to Parquet format with optimizations."""
    csv_path = Path('data/tr_cre.csv')
    parquet_path = Path('data/tr_cre.parquet')
    
    print(f"Loading CSV from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    print(f"Original shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Optimize data types
    print("\nOptimizing data types...")
    
    # Keep Period as integer for now - will be converted to datetime on load
    if 'Period' in df.columns:
        df['Period'] = df['Period'].astype('int32')
    
    # Convert string columns to category to save space
    categorical_cols = ['LEI_Code', 'NSA', 'Item', 'Label', 'Portfolio', 'Country', 'Sheet', 'Unit']
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype('category')
            print(f"  {col}: category")
    
    # Ensure Amount is float32
    if 'Amount' in df.columns:
        df['Amount'] = df['Amount'].astype('float32')
        print(f"  Amount: float32")
    
    # Save as Parquet with compression
    print(f"\nSaving to {parquet_path}...")
    df.to_parquet(parquet_path, engine='pyarrow', compression='snappy', index=False)
    
    # Verify the saved file
    print("\nVerifying saved file...")
    df_loaded = pd.read_parquet(parquet_path)
    print(f"Loaded shape: {df_loaded.shape}")
    print(f"Period values: {sorted(df_loaded['Period'].unique())}")
    
    # Check file sizes
    csv_size = csv_path.stat().st_size / (1024 * 1024)
    parquet_size = parquet_path.stat().st_size / (1024 * 1024)
    
    print(f"\nFile sizes:")
    print(f"  CSV: {csv_size:.2f} MB")
    print(f"  Parquet: {parquet_size:.2f} MB")
    print(f"  Reduction: {(1 - parquet_size/csv_size) * 100:.1f}%")
    
    print("\n✓ Conversion complete!")

if __name__ == '__main__':
    convert_to_parquet()
