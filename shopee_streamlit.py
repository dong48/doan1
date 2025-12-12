import numpy as np
import matplotlib.pyplot as plt
import squarify
import streamlit as st
import pandas as pd
import plotly.express as px

# Cấu hình chungchung
st.set_page_config(
    page_title="Phân tích hành vi tiêu dùng Shopee",
    layout="wide"
)
# Nền trắng – chữ đen 
st.markdown(
    """
    <style>
        /* Toàn bộ app nền trắng, chữ đen */
        .stApp {
            background-color: #FFFFFF;
            color: #000000;
        }

        /* Chữ trong các tab: màu đen, dễ đọc */
        .stTabs [role="tab"] {
            color: #000000 !important;
            font-weight: 500;
        }

        /* Tab đang được chọn: gạch chân đen */
        .stTabs [role="tab"][aria-selected="true"] {
            border-bottom: 2px solid #000000 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Hàm đọc dữ liệu 
@st.cache_data
def load_data(path: str = "shopee_clean.csv") -> pd.DataFrame:
    """
    Đọc dữ liệu đã làm sạch và tách thêm ngành chính / ngành con
    giống hệt notebook phân tích.
    """
    df = pd.read_csv(path)

    # Tách chuỗi ngành hàng
    tach_nganh = df["nganh_hang"].astype(str).str.split("|")

    def lay_nganh_chinh(ds):
        return ds[1].strip() if len(ds) >= 2 else "Khác"

    def lay_nganh_con(ds):
        return ds[2].strip() if len(ds) >= 3 else "Khác"

    df["nganh_chinh"] = tach_nganh.apply(lay_nganh_chinh)
    df["nganh_con"] = tach_nganh.apply(lay_nganh_con)

    return df
df = load_data()
#  MENU
with st.sidebar:
    st.header("MENU")

    main_section = st.radio(
        "Chọn PHẦN:",
        (
            "PHẦN 1: TỔNG QUAN",
            "PHẦN 2: PHÂN TÍCH BIỂU ĐỒ",
            "PHẦN 3: TỔNG KẾT"
        )
    )

    if main_section == "PHẦN 1: TỔNG QUAN":
        sub_section = st.radio(
            "Chọn mục:",
            (
                "1.1 Giới thiệu & Dữ liệu gốc",
                "1.2 Quy trình & Xử lý dữ liệu"
            )
        )
    elif main_section == "PHẦN 2: PHÂN TÍCH BIỂU ĐỒ":
        sub_section = st.radio(
            "Chọn mục:",
            (
                "2.1 Phân tích ngành hàng bán chạy và cơ cấu ngành hàng",
                "2.2 Đánh giá chất lượng và mức độ phổ biến của ngành hàng",
                "2.3 Phân tích phân khúc người bán và hiệu quả bán hàng"
            )
        )
    else:  # PHẦN 3
        sub_section = st.radio(
            "Chọn mục:",
            (
                "3.1 Kết luận",
                "3.2 Hạn chế & Hướng phát triển"
            )
        )

# TIÊU ĐỀ CHUNG TRÊN MAIN PAGE
st.title("PHÂN TÍCH HÀNH VI TIÊU DÙNG TỪ DỮ LIỆU TMĐT")

# 
# NỘI DUNG THEO TỪNG MỤC
# 

# PHẦN 1: TỔNG QUAN 
if main_section == "PHẦN 1: TỔNG QUAN":

    #  1.1 Giới thiệu & Dữ liệu gốc 
    if sub_section == "1.1 Giới thiệu & Dữ liệu gốc":
        st.header("1.1 Giới thiệu & Dữ liệu gốc")
        
        st.subheader("Giới thiệu đề tài")
        st.markdown(
            """
            Đề tài tập trung **phân tích hành vi tiêu dùng từ dữ liệu bán hàng trên nền tảng
            thương mại điện tử (TMĐT)**, cụ thể là dữ liệu sản phẩm và người bán trên Shopee.

            Mục tiêu chính của bài phân tích là:
            1. **Phân tích ngành hàng bán chạy và cơ cấu ngành hàng** theo ngành chính và ngành con.  
            2. **Đánh giá chất lượng và mức độ phổ biến của ngành hàng** dựa trên điểm đánh giá và lượt đánh giá.  
            3. **Phân tích phân khúc người bán và hiệu quả bán hàng** để gợi ý một số định hướng chiến lược.
            """
        )

        #  TỔNG QUAN BỘ DỮ LIỆU
        st.subheader("Tổng quan bộ dữ liệu sử dụng")

        col1, col2 = st.columns(2)
        with col1:
            so_dong = len(df)
            st.write("**Số dòng:**")
            st.write(f"{so_dong:,}".replace(",", "."))
        with col2:
            so_cot_goc = 6   # hoặc: so_cot_goc = len(mo_ta_cot)
            st.write("**Số biến gốc trong bộ dữ liệu:**")
            st.write(so_cot_goc)

        st.markdown("**Các biến chính trong bộ dữ liệu:**")

        mo_ta_cot = {
            "so_luot_yeu_thich": "Số lượt người dùng bấm yêu thích sản phẩm.",
            "so_luot_danh_gia": "Tổng số lượt đánh giá mà sản phẩm nhận được.",
            "so_luong_ban": "Tổng số lượng sản phẩm đã bán.",
            "ten_nguoi_ban": "Tên shop / người bán trên nền tảng Shopee.",
            "diem_danh_gia": "Điểm đánh giá trung bình của sản phẩm (thang điểm 5).",
            "nganh_hang": (
                "Chuỗi mô tả đường dẫn ngành hàng của sản phẩm trên Shopee, "
                "bao gồm ngành chính và ngành con."
            ),
        }

        mo_ta_df = pd.DataFrame(
            [{"Tên cột": k, "Ý nghĩa": v} for k, v in mo_ta_cot.items()]
        )
        st.table(mo_ta_df)

        # Hiển thị một số dòng dữ liệu mẫu trong expander
        with st.expander("Xem 10 dòng dữ liệu mẫu"):
            st.dataframe(df.head(10), height=300)

    #  1.2 Quy trình & Xử lý dữ liệu 
    elif sub_section == "1.2 Quy trình & Xử lý dữ liệu":
        st.header("1.2 Quy trình & Xử lý dữ liệu")
        st.subheader("Tóm tắt quy trình xử lý dữ liệu")

        st.markdown(
            """
            Trong đồ án này, dữ liệu được xử lý qua ba nhóm bước chính:

            **Bước 1 – Chuẩn bị dữ liệu gốc**

            - Đọc dữ liệu sản phẩm từ file CSV gốc lấy từ Shopee.  
            - Lựa chọn các biến liên quan trực tiếp đến hành vi tiêu dùng và chất lượng sản phẩm.  
            - Đổi tên cột sang tiếng Việt để thuận tiện cho việc trình bày và đọc hiểu.

            **Bước 2 – Làm sạch và chuẩn hóa dữ liệu**

            - Chuẩn hóa các cột dạng đếm (số lượt yêu thích, số lượt đánh giá, số lượng bán):  
              chuyển các giá trị có ký hiệu `k` (nghìn) về dạng số thực.  
            - Ép kiểu số cho các biến định lượng:
              `so_luot_yeu_thich`, `so_luot_danh_gia`, `so_luong_ban`, `diem_danh_gia`.  
            - Xử lý giá trị thiếu:
              - Điền 0 cho các giá trị thiếu ở các cột đếm (yêu thích, đánh giá, bán).  
              - Loại bỏ các bản ghi không có `diem_danh_gia` hợp lệ.  

            **Bước 3 – Chuẩn bị biến phục vụ phân tích**

            - Sử dụng cột `nganh_hang` để tách thành **ngành chính** và **ngành con**
              (phục vụ phân tích cơ cấu ngành hàng ở phần 2.1).  
            - Tính tổng `so_luong_ban` theo `ten_nguoi_ban` để phân khúc người bán
              ở phần 2.3.  
            - Lưu bộ dữ liệu sau khi làm sạch vào file `shopee_clean.csv` và sử dụng thống nhất
              cho toàn bộ các phần phân tích.
            """
        )

        st.markdown("---")
        st.subheader("Kiểm tra nhanh dữ liệu sau khi xử lý")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Số giá trị thiếu theo từng cột:**")
            st.write(df.isnull().sum())

        with col2:
            st.write("**Thống kê mô tả một số biến định lượng:**")
            st.write(
                df[[
                    "so_luot_yeu_thich",
                    "so_luot_danh_gia",
                    "so_luong_ban",
                    "diem_danh_gia"
                ]].describe()
            )
       
#  PHẦN 2: PHÂN TÍCH BIỂU ĐỒ 
elif main_section == "PHẦN 2: PHÂN TÍCH BIỂU ĐỒ":

    #  2.1 Phân tích ngành hàng bán chạy và cơ cấu ngành hàng 
    if sub_section == "2.1 Phân tích ngành hàng bán chạy và cơ cấu ngành hàng":
        st.header("2.1 Phân tích ngành hàng bán chạy và cơ cấu ngành hàng")

        # Tạo 3 tab:
        tab1, tab2, tab3 = st.tabs([
            "Top 10 ngành chính bán chạy nhất",
            "Top 7 ngành con bán chạy nhất trong 6 ngành chính",
            "Cơ cấu ngành con trong ngành (Health & Beauty)"
        ])

        #  TAB 1: TOP 10 NGÀNH CHÍNH BÁN CHẠY NHẤT 
        with tab1:
            st.subheader("2.1.1 Top 10 ngành chính bán chạy nhất")
            nhom_nganh = df.groupby('nganh_chinh', dropna=False)
            tong_theo_nganh = nhom_nganh['so_luong_ban'].sum().reset_index()
            tong_theo_nganh = tong_theo_nganh.sort_values(
                by="so_luong_ban", ascending=False
            ).reset_index(drop=True)

            ten_nganh = tong_theo_nganh['nganh_chinh'].head(10)
            so_luong = tong_theo_nganh['so_luong_ban'].head(10)
            so_luong_chuan_hoa = so_luong / 1_000_000  # về triệu sản phẩm

            fig, ax = plt.subplots(figsize=(11, 6))
            colors = plt.cm.Blues(np.linspace(0.9, 0.3, len(so_luong_chuan_hoa)))

            bars = ax.barh(
                ten_nganh,
                so_luong_chuan_hoa,
                color=colors,
                edgecolor='none',
                height=0.55
            )

            ax.invert_yaxis()
            ax.set_title(
                "Top 10 Ngành Chính Bán Chạy Nhất Trên Shopee",
                fontsize=16,
                fontweight='bold',
                pad=12
            )
            ax.set_xlabel("Tổng số lượng bán (Triệu sản phẩm)", fontsize=12)
            ax.set_ylabel("Ngành chính", fontsize=12)
            ax.grid(axis='x', linestyle='--', alpha=0.35)

            # Hiển thị số lượng thực lên cột 
            for i, v in enumerate(so_luong_chuan_hoa):
                so_thuc = so_luong.iloc[i]
                ax.text(
                    v + max(so_luong_chuan_hoa) * 0.01,
                    i,
                    f"{so_thuc:,.0f}",
                    va='center',
                    fontsize=11
                )

            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            fig.tight_layout()

            st.pyplot(fig)
            with st.expander("Xem nhận xét & ý nghĩa"):
                st.markdown("**Nhận xét:**")
                st.markdown("""
            - Biểu đồ cho thấy cơ cấu số lượng bán trên Shopee tập trung mạnh vào một số ngành hàng thiết yếu như: Health & Beauty, Home & Living, Mobile & Accessories.
            - Ngành Health & Beauty dẫn đầu rõ rệt với hơn 5,5 triệu sản phẩm bán ra, cao hơn đáng kể so với các ngành còn lại.
            - Đặc biệt, nhóm 3 ngành hàng đứng đầu đã chiếm hơn 43% tổng lượng bán của cả top 10, phản ánh xu hướng chi tiêu mạnh mẽ của người tiêu dùng cho các nhu cầu thiết yếu như làm đẹp, sức khỏe, gia dụng, công nghệ.
            - Ở nhóm giữa, các ngành như Men Clothes, Women Clothes, Baby & Toys, Groceries & Pets duy trì mức tiêu thụ ổn định. Trong khi đó, nhóm cuối bảng có số lượng bán khiêm tốn hơn do đặc thù sản phẩm có giá trị cao hoặc vòng đời sử dụng lâu dài nên tần số mua sắm thấp.
            """)

                st.markdown("**Ý nghĩa:**")
                st.markdown("""
            - Là cơ sở để xác định ngành trọng tâm cần ưu tiên khi phân tích và đưa ra quyết định triển khai.
            - Giúp nhận diện mức độ tập trung nhu cầu theo ngành, từ đó định hướng phân bổ nguồn lực cho các ngành đứng đầu.
            """)
            
            with st.expander("Xem bảng dữ liệu Top 10 ngành chính"):
                bang_top10 = tong_theo_nganh.head(10).copy()
                bang_top10["so_luong_ban_trieu"] = bang_top10["so_luong_ban"] / 1_000_000
                bang_top10 = bang_top10.rename(columns={
                    "nganh_chinh": "Ngành chính",
                    "so_luong_ban": "Số lượng bán",
                    "so_luong_ban_trieu": "Số lượng bán (triệu sản phẩm)"
                })
                st.dataframe(bang_top10, use_container_width=True)

        #  TAB 2: TOP 7 NGÀNH CON BÁN CHẠY NHẤT TRONG 6 NGÀNH CHÍNH 
        with tab2:
            st.subheader("2.1.2 Top 7 ngành con bán chạy nhất trong 6 ngành chính")
            nhom_nganh = df.groupby('nganh_chinh', dropna=False)
            tong_theo_nganh = nhom_nganh['so_luong_ban'].sum().reset_index()
            tong_theo_nganh = tong_theo_nganh.sort_values(
                by="so_luong_ban", ascending=False
            ).reset_index(drop=True)
            top6 = tong_theo_nganh.head(6)
            top6_list = top6['nganh_chinh'].tolist()

            # Lọc dữ liệu thuộc 6 ngành chính này
            du_lieu_top6 = df[df["nganh_chinh"].isin(top6_list)].copy()

            # Group theo nganh_con và lấy Top 7
            tong_theo_nganh_con = du_lieu_top6.groupby(
                'nganh_con', as_index=False
            )['so_luong_ban'].sum()
            tong_theo_nganh_con_sorted = tong_theo_nganh_con.sort_values(
                'so_luong_ban', ascending=False
            )
            top7_nganh_con = tong_theo_nganh_con_sorted.head(7)

            ten_nganh_con = top7_nganh_con["nganh_con"]
            so_luong2 = top7_nganh_con["so_luong_ban"]
            so_luong2_chuan_hoa = so_luong2 / 1_000_000

            fig2, ax2 = plt.subplots(figsize=(11, 6))
            colors2 = plt.cm.GnBu(np.linspace(0.9, 0.3, len(so_luong2_chuan_hoa)))

            ax2.barh(
                ten_nganh_con,
                so_luong2_chuan_hoa,
                color=colors2,
                edgecolor='none',
                height=0.55
            )
            ax2.invert_yaxis()
            ax2.set_title(
                "Top 7 Ngành Con Bán Chạy Nhất (Trong 6 Ngành Chính)",
                fontsize=16,
                fontweight='bold',
                pad=12
            )
            ax2.set_xlabel("Tổng số lượng bán (Triệu sản phẩm)", fontsize=12)
            ax2.set_ylabel("Ngành con", fontsize=12)
            ax2.set_xlim(0, max(so_luong2_chuan_hoa) * 1.15)
            ax2.grid(axis='x', linestyle='--', alpha=0.35)

            for i, v in enumerate(so_luong2_chuan_hoa):
                so_thuc = so_luong2.iloc[i]
                ax2.text(
                    v + max(so_luong2_chuan_hoa) * 0.01,
                    i,
                    f"{so_thuc:,.0f}",
                    va='center',
                    fontsize=11
                )

            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            fig2.tight_layout()

            st.pyplot(fig2)
            with st.expander("Xem nhận xét & ý nghĩa"):
                st.markdown("**Nhận xét:**")
                st.markdown("""
            - Ngành **Medical Supplies** có số lượng bán cao nhất với hơn **1,6 triệu** sản phẩm bán ra, phản ánh đây là nhóm hàng thiết yếu gắn liền với nhu cầu chăm sóc sức khỏe hằng ngày và có tần suất mua lại cao.
            - Hai ngành **Home Decor** và **Screen Protectors** đều đạt trên **1,16 triệu** lượt bán, đây là các sản phẩm đặc trưng của TMĐT với ưu điểm kích thước nhỏ gọn, dễ vận chuyển và người tiêu dùng dễ dàng ra quyết định mua sắm nhanh.
            - Các ngành con còn lại như **Feeding & Nursing, Pants, Plus Size, Audio** có tổng số lượng bán dao động khoảng **0,7–0,9 triệu** sản phẩm, cho thấy nhu cầu mua sắm khá đa dạng giữa các nhóm hàng.
            - Tổng số lượng bán của top 7 ngành con này chỉ chiếm khoảng **23,15%** toàn bộ dữ liệu. Điều này cho thấy thị trường Shopee tuân theo quy luật “đuôi dài”, trong đó phần lớn số lượng bán còn lại đến từ hàng nghìn sản phẩm và ngành hàng khác, chứ không chỉ tập trung hoàn toàn vào vài nhóm đứng đầu.
            """)

                st.markdown("**Ý nghĩa:**")
                st.markdown("""
            - Đi từ ngành chính xuống ngành con để xác định nhóm sản phẩm cụ thể đang kéo số lượng bán trong các ngành dẫn đầu.
            - Cung cấp căn cứ để chọn ngành con nổi bật, ngành mũi nhọn và đồng thời cho thấy thị trường có nhu cầu đa dạng, không chỉ tập trung tuyệt đối vào một vài nhóm.
            """)
            with st.expander("Xem bảng dữ liệu Top 7 ngành con"):
                bang_top7 = top7_nganh_con.copy()
                bang_top7["so_luong_ban_trieu"] = bang_top7["so_luong_ban"] / 1_000_000
                bang_top7 = bang_top7.rename(columns={
                    "nganh_con": "Ngành con",
                    "so_luong_ban": "Số lượng bán",
                    "so_luong_ban_trieu": "Số lượng bán (triệu sản phẩm)"
                })
                st.dataframe(bang_top7, use_container_width=True)
        #  TAB 3: CƠ CẤU NGÀNH CON TRONG HEALTH & BEAUTY ===
        with tab3:
            st.subheader("2.1.3 Cơ cấu ngành con trong ngành Health & Beauty")
            nganh_focus = "Health & Beauty"
            du_lieu_focus = df[df["nganh_chinh"] == nganh_focus]

            if du_lieu_focus.empty:
                st.warning(f"Không tìm thấy dữ liệu cho ngành {nganh_focus}.")
            else:
                tong_theo_con_trong_nganh = (
                    du_lieu_focus
                    .groupby("nganh_con")["so_luong_ban"]
                    .sum()
                    .sort_values(ascending=False)
                    .reset_index()
                )

                kich_thuoc = []
                ten_nganh_con_focus = []
                for _, dong in tong_theo_con_trong_nganh.iterrows():
                    ten = dong["nganh_con"]
                    gia_tri = dong["so_luong_ban"]
                    ten_nganh_con_focus.append(ten)
                    kich_thuoc.append(gia_tri)
                kich_thuoc = np.array(kich_thuoc)

                def dinh_dang_gia_tri(v):
                    if v >= 1_000_000:
                        s = f"{v/1_000_000:.2f}"
                        return s.replace(".", ",") + "M"
                    elif v >= 1_000:
                        s = f"{v/1_000:.2f}"
                        return s.replace(".", ",") + "K"
                    else:
                        s = f"{v:.2f}"
                        return s.replace(".", ",")

                nhan = [
                    f"{ten}\n{dinh_dang_gia_tri(v)}"
                    for ten, v in zip(ten_nganh_con_focus, kich_thuoc)
                ]

                kich_thuoc_chuan_hoa = squarify.normalize_sizes(
                    kich_thuoc, 100, 100
                )
                ds_hinh = squarify.squarify(
                    kich_thuoc_chuan_hoa, 0, 0, 100, 100
                )

                fig3, ax3 = plt.subplots(figsize=(12, 7))
                mau_sac = plt.cm.Greens(
                    np.linspace(0.85, 0.25, len(kich_thuoc))
                )

                nguong = 200_000  

                for hinh, mau, text, gia_tri in zip(
                    ds_hinh, mau_sac, nhan, kich_thuoc
                ):
                    x, y, dx, dy = (
                        hinh["x"], hinh["y"], hinh["dx"], hinh["dy"]
                    )
                    ax3.add_patch(
                        plt.Rectangle(
                            (x, y),
                            dx,
                            dy,
                            facecolor=mau,
                            edgecolor="white",
                        )
                    )
                    mau_chu = "white" if gia_tri >= nguong else "black"
                    ax3.text(
                        x + dx / 2,
                        y + dy / 2,
                        text,
                        ha="center",
                        va="center",
                        fontsize=9,
                        color=mau_chu,
                    )

                ax3.set_axis_off()
                ax3.set_xlim(0, 100)
                ax3.set_ylim(0, 100)
                fig3.subplots_adjust(left=0, right=1, top=0.88, bottom=0)
                ax3.set_title(
                    f"Cơ Cấu Ngành Con Trong Ngành {nganh_focus}",
                    fontsize=16,
                    fontweight="bold",
                    pad=18,
                )

                st.pyplot(fig3)
            with st.expander("Xem nhận xét & ý nghĩa"):
                st.markdown("**Nhận xét:**")
                st.markdown("""
            - Ngành **Medical Supplies** chiếm diện tích lớn nhất với số lượng bán ra khoảng **1,61 triệu** sản phẩm. Cho thấy đây là ngành con có vai trò quan trọng trong toàn bộ ngành **Health & Beauty** được người dùng Shopee mua với tần suất cao.
            - Các ngành như **Eye Make Up, Personal Pleasure, Skincare, Pedicure & Manicure, Bath & Body, Face Make Up** có diện tích ở tương đối lớn và khá đồng đều với số lượng bán dao động từ khoảng **0,22–0,53 triệu** sản phẩm. Đây phần lớn là các sản phẩm chăm sóc và làm đẹp được sử dụng hằng ngày với nhu cầu mua lại thường xuyên.
            - Những ngành con còn lại tuy không cao bằng những nhóm trên, nhưng phản ánh mức độ đa dạng của ngành chính **Health & Beauty**.
            """)

                st.markdown("**Ý nghĩa:**")
                st.markdown("""
            - Hỗ trợ nhìn nhanh cơ cấu của một ngành lớn **Health & Beauty**, từ đó xác định ngành con chủ lực và các ngành con còn lại.
            - Là căn cứ để ưu tiên phân tích và định hướng chiến lược trong chính ngành **Health & Beauty** theo hướng tập trung vào nhóm có nhu cầu mua thường xuyên, đồng thời vẫn phản ánh tính đa dạng của ngành.
            """)
            with st.expander("Xem bảng dữ liệu cơ cấu ngành con (Health & Beauty)"):
                bang_hb = tong_theo_con_trong_nganh.copy()
                tong_hb = bang_hb["so_luong_ban"].sum()
                bang_hb["ty_trong_%"] = bang_hb["so_luong_ban"] / tong_hb * 100

                bang_hb = bang_hb.rename(columns={
                    "nganh_con": "Ngành con",
                    "so_luong_ban": "Số lượng bán"
                })
                # Sắp xếp lại cho đẹp
                bang_hb = bang_hb[["Ngành con", "Số lượng bán", "ty_trong_%"]]
                st.dataframe(bang_hb, use_container_width=True)
    #  2.2 Đánh giá chất lượng và mức độ phổ biến của ngành hàng 
    elif sub_section == "2.2 Đánh giá chất lượng và mức độ phổ biến của ngành hàng":
        st.header("2.2 Đánh giá chất lượng và mức độ phổ biến của ngành hàng")
        danh_gia_theo_nganh = (
            df.groupby("nganh_chinh", dropna=False)
              .agg({
                  "diem_danh_gia": "mean",
                  "so_luot_danh_gia": "sum"
              })
              .reset_index()
        )

        danh_gia_theo_nganh = danh_gia_theo_nganh.rename(columns={
            "diem_danh_gia": "diem_tb",
            "so_luot_danh_gia": "tong_luot_danh_gia"
        })

        # Tính trung vị
        median_diem = danh_gia_theo_nganh["diem_tb"].median()
        median_luot = danh_gia_theo_nganh["tong_luot_danh_gia"].median()

        # Phân mức độ
        danh_gia_theo_nganh["muc_do_hai_long"] = np.where(
            danh_gia_theo_nganh["diem_tb"] >= median_diem,
            "Cao",
            "Thấp"
        )

        danh_gia_theo_nganh["muc_do_pho_bien"] = np.where(
            danh_gia_theo_nganh["tong_luot_danh_gia"] >= median_luot,
            "Cao",
            "Thấp"
        )

        def phan_nhom(row):
            if row["muc_do_pho_bien"] == "Cao" and row["muc_do_hai_long"] == "Cao":
                return "Nhóm 1: Cao - Cao (Ngành mạnh)"
            elif row["muc_do_pho_bien"] == "Cao" and row["muc_do_hai_long"] == "Thấp":
                return "Nhóm 2: Cao - Thấp (Ngành tiềm năng)"
            elif row["muc_do_pho_bien"] == "Thấp" and row["muc_do_hai_long"] == "Cao":
                return "Nhóm 3: Thấp - Cao (Ngành rủi ro)"
            else:
                return "Nhóm 4: Thấp - Thấp (Ngành yếu)"

        danh_gia_theo_nganh["nhom_nganh"] = danh_gia_theo_nganh.apply(phan_nhom, axis=1)

        # Tạo cột x ảo (nén trục X giống notebook)
        danh_gia_theo_nganh["x_ao"] = danh_gia_theo_nganh["tong_luot_danh_gia"] ** 0.25

        # Tạo kích thước bong bóng theo log(lượt đánh giá)
        size_raw = np.log10(danh_gia_theo_nganh["tong_luot_danh_gia"] + 1)
        size_min, size_max = size_raw.min(), size_raw.max()
        if size_max > size_min:
            size_final = 18 + (size_raw - size_min) / (size_max - size_min) * (60 - 18)
        else:
            size_final = np.full_like(size_raw, 24)

        danh_gia_theo_nganh["size_bubble"] = size_final

        #  2. VẼ BIỂU ĐỒ BONG BÓNG (MA TRẬN CHIẾN LƯỢC) 
        st.subheader("2.2.1 Ma trận chiến lược: Chất lượng × Quy mô")

        color_map = {
            "Nhóm 1: Cao - Cao (Ngành mạnh)": "#2E7D32",   # xanh lá
            "Nhóm 2: Cao - Thấp (Ngành tiềm năng)": "#1565C0",  # xanh dương
            "Nhóm 3: Thấp - Cao (Ngành rủi ro)": "#EF6C00",     # cam
            "Nhóm 4: Thấp - Thấp (Ngành yếu)": "#C62828"       # đỏ
        }

        fig = px.scatter(
            danh_gia_theo_nganh,
            x="x_ao",
            y="diem_tb",
            size="size_bubble",
            color="nhom_nganh",
            hover_name="nganh_chinh",
            size_max=60,
            color_discrete_map=color_map,
            labels={
                "x_ao": "Quy mô (lượt đánh giá, scale căn bậc 4)",
                "diem_tb": "Điểm đánh giá trung bình",
                "nhom_nganh": "Nhóm chiến lược"
            },
        )

        # Thêm đường median 
        x_min, x_max = danh_gia_theo_nganh["x_ao"].min(), danh_gia_theo_nganh["x_ao"].max()
        median_x_ao = median_luot ** 0.25

        fig.add_shape(
            type="line",
            x0=x_min, x1=x_max,
            y0=median_diem, y1=median_diem,
            line=dict(color="gray", dash="dash")
        )

        fig.add_shape(
            type="line",
            x0=median_x_ao, x1=median_x_ao,
            y0=danh_gia_theo_nganh["diem_tb"].min(),
            y1=danh_gia_theo_nganh["diem_tb"].max(),
            line=dict(color="gray", dash="dash")
        )

        fig.update_layout(
            title={
                "text": "Ma trận chiến lược: Chất lượng và Quy mô theo ngành hàng",
                "x": 0.5,
                "xanchor": "center"
            },
            legend_title_text="Nhóm ngành",
            hovermode="closest"
        )

        # Ghi chú 4 góc (Ngành mạnh / tiềm năng / rủi ro / yếu)
        fig.add_annotation(
            x=x_max, y=danh_gia_theo_nganh["diem_tb"].max(),
            text="Ngành mạnh\n(Cao - Cao)",
            showarrow=False,
            align="right"
        )
        fig.add_annotation(
            x=x_max, y=danh_gia_theo_nganh["diem_tb"].min(),
            text="Ngành tiềm năng\n(Cao - Thấp)",
            showarrow=False,
            align="right"
        )
        fig.add_annotation(
            x=x_min, y=danh_gia_theo_nganh["diem_tb"].max(),
            text="Ngành rủi ro\n(Thấp - Cao)",
            showarrow=False,
            align="left"
        )
        fig.add_annotation(
            x=x_min, y=danh_gia_theo_nganh["diem_tb"].min(),
            text="Ngành yếu\n(Thấp - Thấp)",
            showarrow=False,
            align="left"
        )

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Xem nhận xét & ý nghĩa"):
            st.markdown("**Nhận xét:**")
            st.markdown("""
        - Biểu đồ cho thấy các ngành hàng được chia thành bốn nhóm rõ ràng theo **điểm đánh giá trung bình** và **tổng lượt đánh giá**. Nhóm **Cao – Cao** (màu xanh lá) vừa có nhiều lượt đánh giá vừa được điểm đánh giá cao, đây là ngành mạnh, đang thu hút nhiều khách và vẫn giữ được mức độ hài lòng tốt, nên cần được ưu tiên duy trì và hỗ trợ phát triển.
        - Nhóm **Cao – Thấp** (màu xanh dương) có điểm số đẹp nhưng ít lượt đánh giá, thể hiện các ngành còn mới hoặc ngành chưa được nhiều người biết đến; nếu được đẩy mạnh quảng bá, nhóm này có thể trở thành ngành mạnh trong tương lai.
        - Ngược lại, nhóm **Thấp – Cao** (màu cam) có quy mô lớn nhưng điểm đánh giá thấp hơn, cho thấy nguy cơ về trải nghiệm của khách hàng, cần sớm xem lại chất lượng sản phẩm và dịch vụ.
        - Cuối cùng, nhóm **Thấp – Thấp** (màu đỏ) vừa ít khách vừa điểm chưa cao, hiện chưa phải là nhóm ưu tiên đầu tư.
        """)

            st.markdown("**Ý nghĩa:**")
            st.markdown("""
        - Giúp phân nhóm ngành hàng thành bốn nhóm chiến lược theo ngưỡng trung vị, để ra quyết định ưu tiên rõ ràng thay vì đánh giá theo cảm tính.
        - Là cơ sở hành động theo đúng logic trong bài:
        - **Cao–Cao:** ưu tiên duy trì và phát triển.
        - **Cao–Thấp:** có thể đẩy quảng bá để tăng phổ biến.
        - **Thấp–Cao:** cần xem lại chất lượng và dịch vụ.
        - **Thấp–Thấp:** chưa phải nhóm ưu tiên đầu tư.
        """)
        #  3. BẢNG DỮ LIỆU TÓM TẮT
        st.subheader("2.2.2 Bảng tổng hợp ngành hàng theo nhóm chiến lược")

        with st.expander("Xem bảng dữ liệu chi tiết theo ngành chính"):
            bang_hien_thi = danh_gia_theo_nganh.copy()
            bang_hien_thi = bang_hien_thi[[
                "nganh_chinh",
                "diem_tb",
                "tong_luot_danh_gia",
                "muc_do_hai_long",
                "muc_do_pho_bien",
                "nhom_nganh"
            ]].sort_values("tong_luot_danh_gia", ascending=False)

            bang_hien_thi = bang_hien_thi.rename(columns={
                "nganh_chinh": "Ngành chính",
                "diem_tb": "Điểm TB",
                "tong_luot_danh_gia": "Tổng lượt đánh giá",
                "muc_do_hai_long": "Mức độ hài lòng",
                "muc_do_pho_bien": "Mức độ phổ biến",
                "nhom_nganh": "Nhóm chiến lược"
            })
            st.dataframe(bang_hien_thi, use_container_width=True)

        with st.expander("Thống kê nhanh số ngành trong từng nhóm"):
            thong_ke_nhom = (
                danh_gia_theo_nganh["nhom_nganh"]
                .value_counts()
                .rename_axis("Nhóm ngành")
                .reset_index(name="Số lượng ngành")
            )
            st.table(thong_ke_nhom)
    # 2.3 Phân tích phân khúc người bán và hiệu quả bán hàng 
    elif sub_section == "2.3 Phân tích phân khúc người bán và hiệu quả bán hàng":
        st.header("2.3 Phân tích phân khúc người bán và hiệu quả bán hàng")
        # 1. TÍNH TOÁN PHÂN KHÚC NGƯỜI BÁN
        # Tổng số lượng bán theo từng người bán
        nguoi_ban = (
            df.groupby("ten_nguoi_ban", as_index=False)["so_luong_ban"]
              .sum()
              .rename(columns={"so_luong_ban": "tong_so_luong_ban"})
        )

        # Sắp xếp giảm dần theo tổng số lượng bán
        nguoi_ban = nguoi_ban.sort_values(
            "tong_so_luong_ban", ascending=False
        ).reset_index(drop=True)

        n = len(nguoi_ban)

        # Chia ngưỡng phân khúc (xấp xỉ như notebook: 1% – 10% – 40%)
        cut1 = int(np.ceil(n * 0.01))   # Top 1%
        cut2 = int(np.ceil(n * 0.10))   # Top 10%
        cut3 = int(np.ceil(n * 0.40))   # Top 40%

        def gan_phan_khuc(idx):
            if idx < cut1:
                return "Xuất sắc (Top 1%)"
            elif idx < cut2:
                return "Tiềm năng (Top 9% tiếp)"
            elif idx < cut3:
                return "Khá (Top 30% tiếp)"
            else:
                return "Trung bình (60% cuối)"

        nguoi_ban["phan_khuc"] = nguoi_ban.index.map(gan_phan_khuc)

        # Thứ tự hiển thị cố định cho đẹp
        order_segments = [
            "Xuất sắc (Top 1%)",
            "Tiềm năng (Top 9% tiếp)",
            "Khá (Top 30% tiếp)",
            "Trung bình (60% cuối)"
        ]
        # Tạo 3 tab:
        tab1, tab2, tab3 = st.tabs([
            "Phân bố số lượng người bán theo phân khúc",
            "Đóng góp tổng số lượng bán theo phân khúc người bán",
            "Số lượng bán trung bình trên 1 người bán theo phân khúc"
        ])

        #  TAB 1: PHÂN BỐ SỐ LƯỢNG NGƯỜI BÁN THEO PHÂN KHÚC 
        with tab1:
            st.subheader("2.3.1 Phân bố số lượng người bán theo phân khúc")
            dem_theo_nhom = (
                nguoi_ban["phan_khuc"]
                .value_counts()
                .reindex(order_segments)
                .dropna()
                .rename_axis("Phân khúc")
                .reset_index(name="Số lượng người bán")
            )

            tong_seller = dem_theo_nhom["Số lượng người bán"].sum()
            dem_theo_nhom["Tỷ lệ (%)"] = (
            dem_theo_nhom["Số lượng người bán"] / tong_seller * 100
            )

            # Vẽ biểu đồ
            fig, ax = plt.subplots(figsize=(9, 6))
            x = np.arange(len(dem_theo_nhom))
            y = dem_theo_nhom["Số lượng người bán"].values

            bars = ax.bar(x, y, width=0.6)

            ax.set_xticks(x)
            ax.set_xticklabels(dem_theo_nhom["Phân khúc"], rotation=10)
            ax.set_ylabel("Số lượng người bán", fontsize=12)
            ax.set_title("Phân bố số lượng người bán theo phân khúc", fontsize=16)
            ax.grid(axis="y", linestyle="--", alpha=0.3)

            for i, v in enumerate(y):
                ax.text(
                    i,
                    v + max(y) * 0.02,
                    f"{v} ({dem_theo_nhom['Tỷ lệ (%)'].iloc[i]:.1f}%)",
                    ha="center",
                    va="bottom",
                    fontsize=10,
                )

            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            fig.tight_layout()

            st.pyplot(fig)

            with st.expander("Xem nhận xét & ý nghĩa"):
                st.markdown("**Nhận xét:**")
                st.markdown("""
            - Quan sát biểu đồ, số lượng người bán trên sàn có dạng gần giống một “kim tự tháp”.
            - Ở tầng dưới cùng là hai nhóm **Trung Bình** và **Khá**, chiếm khoảng **90%** tổng số người bán. Điều này cho thấy rất nhiều người tham gia bán hàng trên TMĐT, ai cũng có thể làm người bán hàng nên mức độ cạnh tranh ở nhóm này khá cao.
            - Ngược lại, hai nhóm ở phía trên là **Xuất Sắc** và **Tiềm Năng** chỉ chiếm khoảng **10%** tổng số người bán. Mặc dù số lượng không nhiều, nhưng đây là những người bán hoạt động tốt hơn, thường có những lượt bán cao và ổn định hơn so với mặt bằng chung.
            - Từ số liệu trên, có thể thấy để lọt vào nhóm **Xuất Sắc** không hề dễ, chỉ một tỷ lệ rất nhỏ người bán đạt được mức này. Phần lớn người bán vẫn đang ở quy mô trung bình, cho thấy sự chênh lệch khá lớn giữa nhóm bán hàng tốt và phần còn lại của thị trường.
            """)

                st.markdown("**Ý nghĩa:**")
                st.markdown("""
            - Giúp nhìn được bức tranh tổng thể cấu trúc người bán theo dạng “kim tự tháp”, qua đó đánh giá thực tế mức độ cạnh tranh giữa các nhóm.
            - Thể hiện rõ khoảng cách giữa nhóm bán tốt và phần còn lại, làm căn cứ để định hướng mục tiêu “lên phân khúc” trong phân tích người bán.
            """)
            with st.expander("Xem bảng dữ liệu phân bố theo phân khúc"):
                st.dataframe(dem_theo_nhom, use_container_width=True)
        #  TAB 2: ĐÓNG GÓP TỔNG SỐ LƯỢNG BÁN THEO PHÂN KHÚC 
        with tab2:
            st.subheader("2.3.2 Đóng góp tổng số lượng bán theo phân khúc người bán")
            tong_theo_nhom = (
                nguoi_ban.groupby("phan_khuc")["tong_so_luong_ban"]
                .sum()
                .reindex(order_segments)
                .dropna()
                .rename_axis("Phân khúc")
                .reset_index()
            )

            tong_toan_bo = tong_theo_nhom["tong_so_luong_ban"].sum()
            tong_theo_nhom["Tỷ trọng (%)"] = (
                tong_theo_nhom["tong_so_luong_ban"] / tong_toan_bo * 100
            )
            tong_theo_nhom["Số lượng bán (triệu)"] = (
                tong_theo_nhom["tong_so_luong_ban"] / 1_000_000
            )

            fig2, ax2 = plt.subplots(figsize=(9, 6))

            y_labels = tong_theo_nhom["Phân khúc"]
            x_values = tong_theo_nhom["Số lượng bán (triệu)"].values

            bars2 = ax2.barh(y_labels, x_values, height=0.55)

            ax2.set_xlabel("Tổng số lượng bán (triệu sản phẩm)", fontsize=12)
            ax2.set_title(
                "Đóng góp tổng số lượng bán theo phân khúc người bán",
                fontsize=16,
            )
            ax2.grid(axis="x", linestyle="--", alpha=0.3)

            for i, v in enumerate(x_values):
                phan_tram = tong_theo_nhom["Tỷ trọng (%)"].iloc[i]
                ax2.text(
                    v + max(x_values) * 0.02,
                    i,
                    f"{v:.2f}M ({phan_tram:.1f}%)",
                    va="center",
                    fontsize=10,
                )

            ax2.spines["top"].set_visible(False)
            ax2.spines["right"].set_visible(False)
            fig2.tight_layout()

            st.pyplot(fig2)
            with st.expander("Xem nhận xét & ý nghĩa"):
                st.markdown("**Nhận xét:**")
                st.markdown("""
            - Qua quan sát, nhóm thấy sự đóng góp về lượt bán giữa các phân khúc có sự chênh lệch khá rõ. Nhóm **Khá** là nhóm đóng góp nhiều nhất, với khoảng **13,4 triệu** lượt bán chiếm **42,1%**, chứ không phải nhóm **Xuất Sắc**. Điều này cho thấy hoạt động đóng của sàn không chỉ dựa vào một vài shop top đầu mà chủ yếu dựa vào nhóm các shop tầm trung nhưng bán ổn định.
            - Nhóm **Xuất Sắc** đứng thứ hai với khoảng **11,85 triệu** chiếm **37,4%**, trong khi chỉ chiếm **1%** số lượng người bán. Như vậy, chỉ một tỷ lệ rất nhỏ người bán nhưng lại đóng góp hơn 1/3 lượng hàng bán ra, cho thấy hiệu quả bán hàng của nhóm này cao hơn hẳn so với mặt bằng chung.
            - Ngược lại, hai nhóm **Trung Bình** và **Tiềm Năng** đóng góp ít hơn nhiều dù số lượng người bán khá đông. Cho thấy nhiều người bán vẫn ở quy mô nhỏ, bán không được nhiều đơn.
            """)

                st.markdown("**Ý nghĩa:**")
                st.markdown("""
            - Cho biết nhóm phân khúc nào đang đóng góp chính vào tổng lượt bán, giúp xác định “động lực doanh số” của thị trường người bán.
            - Thể hiện rõ ý trong bài: tăng trưởng không chỉ phụ thuộc nhóm top, mà còn phụ thuộc đáng kể vào nhóm tầm trung bán ổn định.
            """)
            with st.expander("Xem bảng dữ liệu đóng góp theo phân khúc"):
                bang2 = tong_theo_nhom.rename(columns={
                    "tong_so_luong_ban": "Tổng số lượng bán"
                })
                st.dataframe(bang2, use_container_width=True)
        #  TAB 3: SỐ LƯỢNG BÁN TRUNG BÌNH / 1 NGƯỜI BÁN THEO PHÂN KHÚC 
        with tab3:
            st.subheader("2.3.3 Số lượng bán trung bình trên 1 người bán theo phân khúc")
            ban_trung_binh = (
                nguoi_ban.groupby("phan_khuc")["tong_so_luong_ban"]
                .mean()
                .reindex(order_segments)
                .dropna()
                .rename_axis("Phân khúc")
                .reset_index()
            )

            ban_trung_binh["Số lượng bán TB (nghìn)"] = (
                ban_trung_binh["tong_so_luong_ban"] / 1_000
            )

            fig3, ax3 = plt.subplots(figsize=(9, 6))

            x3 = np.arange(len(ban_trung_binh))
            y3 = ban_trung_binh["Số lượng bán TB (nghìn)"].values

            bars3 = ax3.bar(x3, y3, width=0.6)

            ax3.set_xticks(x3)
            ax3.set_xticklabels(ban_trung_binh["Phân khúc"], rotation=10)
            ax3.set_ylabel("Số lượng bán trung bình (nghìn sản phẩm/người bán)", fontsize=12)
            ax3.set_title(
                "Số lượng bán trung bình trên 1 người bán theo phân khúc",
                fontsize=16,
            )
            ax3.grid(axis="y", linestyle="--", alpha=0.3)

            for i, v in enumerate(y3):
                ax3.text(
                    i,
                    v + max(y3) * 0.03,
                    f"{v:.1f}",
                    ha="center",
                    va="bottom",
                    fontsize=10,
                )

            ax3.spines["top"].set_visible(False)
            ax3.spines["right"].set_visible(False)
            fig3.tight_layout()

            st.pyplot(fig3)
            with st.expander("Xem nhận xét & ý nghĩa"):
                st.markdown("**Nhận xét:**")
                st.markdown("""
            - Biểu đồ cho thấy sự áp đảo của phân khúc **Xuất Sắc** với trung bình **136,2K** lượt bán trên một người bán, gấp hơn **8 lần** nhóm **Khá** và hơn **60 lần** nhóm **Trung Bình**. Điều này cho thấy nhóm Xuất Sắc không thắng bởi số đông mà thắng nhờ khả năng bán hàng vượt trội.
            - Dù ở Biểu đồ 6 nhóm **Khá** đóng góp tổng số lượng bán cao nhất, nhưng nhìn sang biểu đồ này có thể thấy mức bán trung bình của nhóm Khá vẫn còn cách khá xa nhóm Xuất Sắc. Điều này cho thấy nhóm Khá chủ yếu mạnh về số lượng người bán, chứ hiệu quả trên từng người bán chưa tối ưu.
            - Nhóm **Tiềm Năng** chỉ đạt khoảng **0,2K**, thậm chí thấp hơn nhóm Trung Bình. Có thể đây là những người bán mới, bán hàng ngách hoặc chưa có nhiều khách truy cập nên họ bán được rất ít. Về lâu dài, nếu được hỗ trợ tốt hơn, nhóm này có thể là nguồn dự phòng để phát triển lên nhóm Khá hoặc Xuất Sắc.
            - Biểu đồ cho thấy khoảng cách từ nhóm **Khá** và **Xuất Sắc** đang là khá lớn. Để đạt được mức hơn **100K** lượt bán trên một người như nhóm Xuất Sắc là điều không dễ và chỉ tỉ lệ rất nhỏ người bán trên sàn làm được điều đó.
            """)

                st.markdown("**Ý nghĩa:**")
                st.markdown("""
            - Đánh giá hiệu quả bán hàng trên từng người bán, để phân biệt đóng góp do số đông và đóng góp do hiệu suất.
            - Là căn cứ thể hiện rõ chênh lệch hiệu suất giữa các phân khúc và khoảng cách để vươn lên nhóm hiệu quả cao.
            """)
            with st.expander("Xem bảng dữ liệu số lượng bán trung bình theo phân khúc"):
                bang3 = ban_trung_binh.rename(columns={
                    "tong_so_luong_ban": "Số lượng bán TB (đơn vị gốc)"
                })
                st.dataframe(bang3, use_container_width=True)

#  PHẦN 3: TỔNG KẾT 
elif main_section == "PHẦN 3: TỔNG KẾT":

    # 3.1 Kết luận 
    if sub_section == "3.1 Kết luận":
        st.header("3.1 Kết luận")

        st.markdown("""
        ### 3.1.1 Cơ cấu ngành hàng và ngành con theo số lượng bán
        - Nhu cầu mua sắm tập trung vào một số ngành hàng chủ đạo, thể hiện qua top ngành chính bán chạy nhất theo số lượng bán.
        - Khi đi sâu vào ngành con trong nhóm ngành chính dẫn đầu, các ngành con nổi bật đóng góp đáng kể vào tổng lượng bán, đồng thời phản ánh tính đa dạng danh mục trong TMĐT.
        - Riêng ngành **Health & Beauty**, cơ cấu ngành con cho thấy sự phân hóa giữa nhóm ngành con quy mô lớn và các nhóm còn lại, giúp nhận diện rõ các mảng sản phẩm trọng tâm.

        ### 3.1.2. Chất lượng và mức độ phổ biến theo ngành hàng
        - Ma trận chiến lược (chất lượng – quy mô) phân nhóm ngành hàng thành bốn nhóm chiến lược.
        - Cách tiếp cận này làm rõ tương quan giữa **điểm đánh giá** và **độ phổ biến**, hỗ trợ ưu tiên hành động theo từng nhóm (duy trì – mở rộng – cải thiện chất lượng – cân nhắc nguồn lực) thay vì đánh giá theo một chỉ tiêu đơn lẻ.

        ### 3.1.3. Phân khúc người bán và hiệu quả bán hàng
        - Thị trường người bán có sự phân tầng rõ rệt: số lượng người bán phân bố theo các nhóm, đồng thời mức đóng góp tổng số lượng bán giữa các nhóm có khác biệt đáng kể.
        - Chỉ tiêu số lượng bán trung bình trên một người bán phản ánh hiệu suất không đồng đều giữa các phân khúc, giúp làm rõ khoảng cách hiệu quả và đặc trưng của từng nhóm người bán.
        """)


    #  3.2 Hạn chế & Hướng phát triển 
    elif sub_section == "3.2 Hạn chế & Hướng phát triển":
        st.header("3.2 Hạn chế & Hướng phát triển")
        
        with st.expander("3.2.1 Hạn chế (xem chi tiết)"):
            st.markdown("""
            - **Giới hạn về thời gian và phạm vi dữ liệu:** Các kết luận hiện tại chủ yếu mang tính mô tả cho tập dữ liệu đang xét, chưa đủ để khẳng định xu hướng dài hạn hoặc so sánh giữa nhiều thời điểm.
            - **Giới hạn về biến phân tích:** Thiếu các biến như *thời gian, giá/giảm giá, phí vận chuyển, địa chỉ, thương hiệu* nên chưa đánh giá được tác động của các yếu tố này đến số lượng bán.
            - **Giới hạn trong phân khúc người bán:** Phân khúc hiện dựa trên số lượng bán theo người bán, chưa xét thêm các khía cạnh như doanh thu.
            - **Giới hạn về triển khai hệ thống:** Chưa tổ chức theo mô hình **MVC (Model–View–Controller)** nên khả năng mở rộng và bảo trì còn hạn chế.
            - **Chưa có mô hình dự đoán:** Đề tài mới dừng ở mức phân tích mô tả và trực quan hóa, chưa hỗ trợ dự đoán để phục vụ ra quyết định.
            """)
        
        with st.expander("3.2.2 Hướng phát triển (xem chi tiết)"):
            st.subheader("3.2.2 Hướng phát triển")
            st.markdown("""
            - **Mở rộng dữ liệu theo thời gian và phạm vi thu thập** để kiểm chứng tính ổn định của kết quả và đánh giá xu hướng theo thời điểm.
            - **Bổ sung biến phân tích** như *giá, giảm giá, phí vận chuyển, thương hiệu, địa chỉ* để đánh giá sâu hơn các yếu tố ảnh hưởng đến hành vi tiêu dùng và số lượng bán.
            - **Mở rộng tiêu chí phân khúc người bán**, kết hợp thêm các chỉ số như doanh thu ước tính hoặc thước đo hiệu quả khác để phản ánh đầy đủ hơn hiệu quả kinh doanh của từng nhóm.
            - **Chuẩn hóa triển khai theo mô hình MVC**, tách rõ phần xử lý dữ liệu (Model), hiển thị (View) và điều hướng (Controller) nhằm tăng tính modular, dễ bảo trì và thuận lợi khi bổ sung tính năng mới.
            - **Xây dựng mô hình dự đoán và tích hợp vào Streamlit** để người dùng có thể thao tác và nhận kết quả dự đoán trực tiếp trên dashboard.
            """)








