import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { getBook } from "../api";
import Button from "@material-ui/core/Button";

function Book(props) {
  let { bookId } = useParams();
  const history = useNavigate()
  const [book, setBook] = useState({});
  useEffect(async () => {
    let data = await getBook(bookId);
    if (data.message === "Success") {
      setBook(data.data);
    }
  }, [bookId]);
  let discount_text;
  if (book.discount_price) {
    let discount = Math.round((book.discount_price / book.price) * 100);
    if (discount % 10 === 0) {
      discount = discount / 10;
    }
    discount_text = discount + "折" + book.discount_price;
  } else {
    discount_text = "";
  }
  return (
    <>
      <h3>書名： {book.name}</h3>
      <div>作者：{book.author}</div>
      {book.author_original ? (
        <div>原文作者：{book.author_original}</div>
      ) : (
        <></>
      )}
      {book.translator ? <div>譯者： {book.translator}</div> : <></>}
      {book.publishing_house ? (
        <div>出版社：{book.publishing_house}</div>
      ) : (
        <></>
      )}
      {book.publishing_date ? (
        <div>出版日期：{book.publishing_date}</div>
      ) : (
        <></>
      )}
      <div>定價：{book.price}</div>
      {book.discount_price ? <div>優惠價：{discount_text}</div> : <></>}
      {book.expire_date ? <div>優惠期限：{book.expire_date}</div> : <></>}
      {book.ISBN ? <div>ISBN：{book.ISBN}</div> : <></>}
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
  );
}

export default Book;
