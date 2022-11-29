import pandas as pd
from parser import TableParser


def main():
    parser = TableParser()
    table_df = pd.read_excel("data/table_investment_summary.xlsx", skiprows=1)
    sentences = parser.parse(table_df, {"Custo  bruto  de aquisição  (k  R$)"})
    print("\n".join(sentences))

    table_df = pd.read_excel("data/table_calendar.xlsx", skiprows=1)
    sentences = parser.parse(table_df, {"Data"}, item_index=1)
    print("\n".join(sentences))




if __name__ == "__main__":
    main()
