function addToCart(MaSach, TenSach, GiaTien) {
    fetch('/api/cart', {
        method: "post",
        body: JSON.stringify({
            "MaSach": MaSach,
            "TenSach": TenSach,
            "GiaTien": GiaTien
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        console.info(data)
        let d = document.getElementsByClassName("cart-counter")
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity
    }) // js promise
}

function updateCart(MaSach, obj) {
    fetch(`/api/cart/${MaSach}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then((data) => {
        let d = document.getElementsByClassName("cart-counter")
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity

        let a = document.getElementsByClassName("cart-amount")
        for (let i = 0; i < a.length; i++)
            a[i].innerText = data.total_amount.toLocaleString("en-US")
    }).catch(err => console.error(err)) // promise
}

function deleteCart(MaSach) {
    if (confirm("Bạn chắc chắn xóa không?") == true) {
        fetch(`/api/cart/${MaSach}`, {
            method: "delete"
        }).then(res => res.json()).then((data) => {
            let d = document.getElementsByClassName("cart-counter")
            for (let i = 0; i < d.length; i++)
                d[i].innerText = data.total_quantity

            let a = document.getElementsByClassName("cart-amount")
            for (let i = 0; i < a.length; i++)
                a[i].innerText = data.total_amount.toLocaleString("en-US")

            let e = document.getElementById(`cart${MaSach}`)
            e.style.display = "none"
        }).catch(err => console.error(err)) // promise
    }

}

function pay() {
    if (confirm("Bạn chắc chắn thanh toán?") == true) {
        fetch("/api/pay").then(res => res.json()).then(data => {
            if (data.status === 200)
                location.reload();
            else
                alert("Có lỗi xày ra!")
        })
    }
}