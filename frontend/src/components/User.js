import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { getUser, getBook, createOrder, deleteCartItem } from "../api";
import Button from "@material-ui/core/Button";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

function User(props) {
  const userSignIn = props.user;
  let { userId } = useParams();
  const [user, setUser] = useState(null);
  const [cart, setCart] = useState([]);
  const history = useNavigate();

  useEffect(async () => {
    refresh();
  }, [userId]);

  const refresh = async () => {
    let data = await getUser(userId);
    if (data.data) {
      if (data.data.cart == undefined) {
        data.data.cart = [];
      }
      if (data.data.orders == undefined) {
        data.data.orders = [];
      }
      let cart_items = [];
      let _user = data.data;
      for (let i = 0; i < _user.cart.length; i++) {
        let book = await getBook(_user.cart[i].book_id);
        book = book.data;
        let price = book.discount_price ? book.discount_price : book.price;
        cart_items.push({
          book_id: _user.cart[i].book_id,
          number: _user.cart[i].number,
          book: book,
          current_price: price,
        });
      }
      for (let i = 0; i < _user.orders.length; i++) {
        for (let j = 0; j < _user.orders[i].items.length; j++) {
          let book = await getBook(_user.orders[i].items[j].book_id);
          book = book.data;
          _user.orders[i].items[j].name = book.name;
        }
      }
      setUser(_user);
      setCart(cart_items);
    } else {
      setUser(null);
    }
  };

  const handleBuy = async () => {
    let items = [];
    let cart = user.cart;
    let price;
    for (let i = 0; i < cart.length; i++) {
      let book_id = cart[i].book_id;
      let book = await getBook(book_id);
      book = book.data;
      if (book.discount_price) {
        price = book.discount_price;
      } else {
        price = book.price;
      }
      items.push({ book_id: book_id, price: price, number: cart[i].number });
    }
    let res = await createOrder(user.user_id, items);
    if (res.message == "Successfully create") {
      res = await deleteCartItem(user.user_id);
      refresh();
    }
    console.log(res);
  };
  // &&
  // userSignIn !== null &&
  // user.user_id === userSignIn.user_id
  return user !== null ? (
    <>
      <h3>
        姓名： {user.last_name} {user.first_name}
      </h3>
      <div>性別： {user.gender}</div>
      <div>信箱：{user.email}</div>

      <div>電話：{user.phone}</div>

      <div>地址： {user.address ? user.address : ""}</div>

      <div>
        購物車：
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>書名</TableCell>
                <TableCell align="right">數量</TableCell>
                <TableCell align="right">價錢</TableCell>
                <TableCell align="right">總價</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {cart.map((row) => {
                return (
                  <TableRow
                    key={row.book_id}
                    sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                  >
                    <TableCell component="th" scope="row">
                      {row.book.name}
                    </TableCell>
                    <TableCell align="right">{row.number}</TableCell>
                    <TableCell align="right">{row.current_price}</TableCell>
                    <TableCell align="right">
                      {row.current_price * row.number}
                    </TableCell>
                  </TableRow>
                );
              })}
              <TableRow
                key="total"
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <TableCell component="th" scope="row"></TableCell>
                <TableCell align="right"></TableCell>
                <TableCell align="right"></TableCell>
                <TableCell align="right">
                  {cart.reduce(
                    (acc, cur) => cur.current_price * cur.number + acc,
                    0
                  )}
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
      </div>

      <div>
        歷史訂單：
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>訂單標號</TableCell>
                <TableCell align="right">內容</TableCell>
                <TableCell align="right">時間</TableCell>
                <TableCell align="right">總價</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {user.orders.map((row) => {
                return (
                  <TableRow
                    key={row.order_id}
                    sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                  >
                    <TableCell component="th" scope="row">
                      {row.order_id}
                    </TableCell>
                    <TableCell align="right">
                      {row.items.map((ele) => {
                        return (
                          <div>{`${ele.name}: ${ele.price}*${ele.number}`}</div>
                        );
                      })}
                    </TableCell>
                    <TableCell align="right">{row.time}</TableCell>
                    <TableCell align="right">{row.total_price}</TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      </div>
      <Button onClick={handleBuy} color="primary" variant="outlined">
        結帳
      </Button>
      <Button
        onClick={() => {
          history("/");
        }}
        color="primary"
        variant="outlined"
      >
        回主畫面
      </Button>
    </>
  ) : (
    <h1>You don't hace the access to this user.</h1>
  );
}

export default User;
