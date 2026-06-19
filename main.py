class Product:
    def __init__(self, id, name, price, quantity_sold, discount):
        self.id = id
        self.name = name
        self.price = price
        self.quantity_sold = quantity_sold
        self.discount = discount
        self.total_revenue = 0.0
        self.revenue_type = ""

    def calculate_revenue(self):
        revenue = self.price * self.quantity_sold - self.discount
        self.total_revenue = max(0.0, revenue) # Đảm bảo không âm theo yêu cầu đề bài
        return self.total_revenue

    def classify_revenue(self):
        if self.total_revenue < 5000000:
            self.revenue_type = "Thấp"
        elif self.total_revenue < 20000000:
            self.revenue_type = "Trung bình" 
        elif self.total_revenue < 50000000:
            self.revenue_type = "Khá"
        else:
            self.revenue_type = "Cao"

class ProductManager:
    def __init__(self):
        self.products = []

    def _input_number(self, prompt, num_type=float, min_val=0, max_val=None):
        while True:
            try:
                val = num_type(input(prompt))
                if val < min_val or (max_val is not None and val > max_val):
                    print(f"Giá trị phải nằm trong khoảng từ {min_val} đến {max_val} !")
                    continue
                return val
            except ValueError:
                print("Dữ liệu nhập vào phải là số hợp lệ! Vui lòng nhập lại.")

    def add_product(self):
        # Validate mã sản phẩm
        while True:
            id = input("Nhập mã sản phẩm: ").strip()
            if not id:
                print("Mã sản phẩm không được để trống!")
                continue
            if any(p.id == id for p in self.products):
                print("Mã sản phẩm đã tồn tại! Vui lòng nhập mã khác.")
                continue
            break

        # Validate tên sản phẩm
        while True:
            name = input("Nhập tên sản phẩm: ").strip()
            if not name:
                print("Tên sản phẩm không được để trống!")
                continue
            break

        price = self._input_number("Nhập giá sản phẩm: ", float, min_val=0)
        quantity_sold = self._input_number("Nhập số sản phẩm đã bán: ", int, min_val=0, max_val=10000)
        discount = self._input_number("Nhập số tiền giảm giá: ", float, min_val=0)

        new_product = Product(id, name, price, quantity_sold, discount)
        new_product.calculate_revenue()
        new_product.classify_revenue()
        self.products.append(new_product)
        print("Thêm sản phẩm thành công.")

    def show_all(self):
        if not self.products:
            print("Danh sách sản phẩm đang rỗng!")
            return
        print(f"{'Mã SP':<7} | {'Tên sản phẩm':<18} | {'Giá bán':<12} | {'Số lượng':<8} | {'Giảm giá':<12} | {'Doanh thu':<12} | Loại doanh thu")
        print("-" * 90)
        for p in self.products:
            print(f"{p.id:<7} | {p.name:<18} | {p.price:<12,.0f} | {p.quantity_sold:<8} | {p.discount:<12,.0f} | {p.total_revenue:<12,.0f} | {p.revenue_type}")

    def update_product(self):
        id = input("Nhập mã sản phẩm cập nhật: ").strip()
        for product in self.products:
            if product.id == id:
                product.price = self._input_number("Nhập giá sản phẩm mới: ", float, min_val=0)
                product.quantity_sold = self._input_number("Nhập số sản phẩm đã bán mới: ", int, min_val=0, max_val=10000)
                product.discount = self._input_number("Nhập số tiền giảm giá mới: ", float, min_val=0)
                product.calculate_revenue()
                product.classify_revenue()
                print("Cập nhật sản phẩm thành công!")
                return
        print("Không tìm thấy sản phẩm cần cập nhật!")
        
    def delete_product(self):
        id = input("Nhập mã sản phẩm cần xoá: ").strip()
        for product in self.products:
            if product.id == id:
                confirm = input("Bạn có chắc muốn xóa sản phẩm này không? (Y/N): ").strip().upper()
                if confirm == "Y":
                    self.products.remove(product)
                    print("Xóa sản phẩm thành công!")
                elif confirm == "N":
                    print("Đã hủy thao tác xóa!")
                else:
                    print("Lựa chọn không hợp lệ!")
                return
        print("Không tìm thấy sản phẩm cần xoá!")

    def search_product(self):
        name = input("Nhập tên sản phẩm cần tìm kiếm: ").strip().lower()
        result = [p for p in self.products if name in p.name.lower()] 
        
        if not result:
            print("Không tìm thấy sản phẩm phù hợp!")
        else:
            for p in result:
                print(f"{p.id:<7} | {p.name:<18} | {p.price:<12,.0f} | {p.quantity_sold:<8} | {p.discount:<12,.0f} | {p.total_revenue:<12,.0f} | {p.revenue_type}")

    def statistics(self):
        if not self.products:
            print("Chưa có dữ liệu để thống kê!")
            return
        stats = {"Thấp": 0, "Trung bình": 0, "Khá": 0, "Cao": 0}
        for product in self.products:
            if product.revenue_type in stats:
                stats[product.revenue_type] += 1
                
        print("--- THỐNG KÊ SỐ LƯỢNG SẢN PHẨM THEO TỪNG LOẠI DOANH THU ---")
        for key, value in stats.items():
            print(f"{key}: {value}")

def main():
    manager = ProductManager()
    while True:
        choice = input('''
================ MENU ================
1. Hiển thị danh sách sản phẩm
2. Thêm sản phẩm mới
3. Cập nhật sản phẩm
4. Xóa sản phẩm
5. Tìm kiếm sản phẩm
6. Thống kê doanh thu
7. Thoát
=====================================
Nhập lựa chọn của bạn: ''')
        match choice:
            case "1":
                manager.show_all()
            case "2":
                manager.add_product()
            case "3":
                manager.update_product()
            case "4":
                manager.delete_product()
            case "5":
                manager.search_product()
            case "6":
                manager.statistics()
            case "7":
                print("Cảm ơn bạn đã sử dụng hệ thống quản lý sản phẩm!")
                break
            case _:
                print("Lựa chọn không hợp lệ")
if __name__ == "__main__":
    main()