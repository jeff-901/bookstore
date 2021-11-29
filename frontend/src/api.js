/** @format */

import axios from "axios";
require("dotenv").config();
const baseURL = process.env.REACT_APP_baseURL || "http://localhost:4000";
const instance = axios.create({ baseURL: baseURL + "/api" });

const createUser = async (role, first_name, last_name, email, phone, gender, address, password) => {
    const data = await instance.post("/user", {
        role,
        first_name,
        last_name,
        email,
        phone,
        gender,
        address,
        password
    });
    console.log(data)
    return data;
};

const getUser = async (user_id) => {
    const data = await instance.get("/user/" + user_id);
    console.log(data)
    return data;
};

const signIn = async (email, password) => {
    const data = await instance.get("/user/signin",{
        email,
        password
    });
    console.log(data);
    return data;
}

const getBook = async () => {
    const {
        data: { data, message },
    } = await instance.get("/book");
    // console.log(message);
    return data.reverse();
};

const createOrder = async (user_id, items) => {
    const {
        data: { data },
    } = await instance.post(`/order`, {
        user_id,
        items
    });
    // console.log(data);
    return data;
};

const deleteOrder = async (id) => {
    const {
        data: { message },
    } = await instance.delete(`/order/${id}`);
    return message;
};

const getOrder = async (id) => {
    const {
        data: { message },
    } = await instance.get("/order/" + id);
    return message;
};

const listUserOrder = async (id) => {
    const {
        data: { message },
    } = await instance.delete(`/search/order?user_id${id}`);
    return message;
};

const createCartItem = async (userId, bookId, number) => {
    const data = await instance.post("/cart", {
        userId,
        bookId,
        number
    });
    return data;
};

const updateCartItem = async (userId, bookId, number) => {
    const {
        data: { data },
    } = await instance.put("/cart",{
        userId,
        bookId,
        number
    });
    return data;
};

const deleteCartItem = async (userId, bookId) => {
    const {
        data: { message },
    } = await instance.delete("/cart", {
        userId,
        bookId
    });
    return message;
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
};
