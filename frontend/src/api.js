/** @format */

import axios from "axios";
require("dotenv").config();
const baseURL = process.env.REACT_APP_baseURL || "http://127.0.0.1:5000";
const instance = axios.create({ baseURL: baseURL + "/api" });

const createUser = async (
  role,
  first_name,
  last_name,
  email,
  phone,
  gender,
  address,
  password
) => {
  return await instance
    .post("/user", {
      role,
      first_name,
      last_name,
      email,
      phone,
      gender,
      address,
      password,
    })
    .then((data) => {
      return data.data;
    })
    .catch((error) => {
      return error.response.data;
    });
};

const getUser = async (user_id) => {
  return instance
    .get("/user/" + user_id)
    .then((res) => {
      return res.data;
    })
    .catch((error) => {
      return error.response.data;
    });
};

const signIn = async (email, password) => {
  return await instance
    .post("/signin", {
      email,
      password,
    })
    .then((data) => {
      return data.data;
    })
    .catch((error) => {
      return error.response.data;
    });
};

const getBook = async (id) => {
  return await instance
    .get(`/book/${id}`)
    .then((res) => {
      return res.data;
    })
    .catch((error) => {
      return error.response.data;
    });
};

const listBook = async () => {
  return await instance
    .get("/book")
    .then((res) => {
      return res.data;
    })
    .catch((error) => {
      return error.response.data;
    });
};

const searchBook = async () => {
  return await instance
    .get("/book")
    .then((res) => {
      return res.data;
    })
    .catch((error) => {
      return error.response.data;
    });
};

const createOrder = async (user_id, items) => {
  return await instance
    .post(`/order`, {
      user_id,
      items,
    })
    .then((res) => {
      return res.data;
    })
    .catch((error) => {
      return error.response.data;
    });
};

const deleteOrder = async (id) => {
  return await instance
    .delete(`/order/${id}`)
    .then((res) => {
      return res.data;
    })
    .catch((error) => {
      return error.response.data;
    });
};

const getOrder = async (id) => {
  return await instance
    .get("/order/" + id)
    .then((res) => {
      return res.data;
    })
    .catch((error) => {
      return error.response.data;
    });
};

const listUserOrder = async (id) => {
  return await instance
    .delete(`/search/order?user_id=${id}`)
    .then((res) => {
      return res.data;
    })
    .catch((error) => {
      return error.response.data;
    });
};

const createCartItem = async (user_id, book_id, number) => {
  return await instance
    .post("/cart", {
      user_id,
      book_id,
      number,
    })
    .then((res) => {
      return res.data;
    })
    .catch((error) => {
      return error.response.data;
    });
};

const updateCartItem = async (user_id, book_id, number) => {
  return await instance
    .put("/cart", {
      user_id,
      book_id,
      number,
    })
    .then((res) => {
      return res.data;
    })
    .catch((error) => {
      return error.response.data;
    });
};

const deleteCartItem = async (user_id, book_id) => {
  return await instance
    .delete(`/cart?user_id=${user_id}`)
    .then((res) => {
      return res.data;
    })
    .catch((error) => {
      return error.response.data;
    });
};

export {
  createUser,
  signIn,
  getUser,
  createCartItem,
  deleteCartItem,
  updateCartItem,
  createOrder,
  deleteOrder,
  listUserOrder,
  getOrder,
  listBook,
  searchBook,
  getBook,
};
