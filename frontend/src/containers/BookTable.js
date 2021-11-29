import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { makeStyles } from "@material-ui/core/styles";
import IconButton from "@material-ui/core/IconButton";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import { TableContainer } from "@material-ui/core";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TablePagination from "@material-ui/core/TablePagination";
import Paper from "@material-ui/core/Paper";
import Link from "@material-ui/core/Link";
import AddBoxIcon from "@material-ui/icons/AddBox";
import { listBook, createCartItem } from "../api";

const useRowStyles = makeStyles((theme) => ({
  root: {
    "& > *": {
      borderBottom: "unset",
    },
  },
  info: {
    "& > *": {
      borderBottom: "unset",
    },
  },
  tablecell: {
    // padding: "8px 4px 8px 4px",
    paddingLeft: theme.spacing(1),
    paddingRight: theme.spacing(1),
    paddingTop: theme.spacing(2),
    paddingBottom: theme.spacing(2),
    fontSize: "8pt",
    textAlign: "center",
  },
  tablecellRemark: {
    // padding: "8px 4px 8px 4px",
    paddingLeft: theme.spacing(1),
    paddingRight: theme.spacing(1),
    paddingTop: theme.spacing(2),
    paddingBottom: theme.spacing(2),
    fontSize: "8pt",
    textAlign: "left",
  },
  btn: {
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    padding: 0,
  },
}));
function Row(props) {
  const { row } = props;
  const classes = useRowStyles();
  const history = useNavigate();
  let discount_text;
  if (row.discount_price) {
    let discount = Math.round((row.discount_price / row.price) * 100);
    if (discount % 10 === 0) {
      discount = discount / 10;
    }
    discount_text = discount + "折" + row.discount_price;
  } else {
    discount_text = "";
  }

  const handleAddCart = async () => {
    if (props.user === null) {
      props.setAlert({
        open: true,
        severity: "error",
        msg: "You are not sign in",
      });
    } else {
      let res = await createCartItem(props.user.user_id, row.book_id, 1);
      if (res.message === "Successfully create") {
        props.setAlert({
          open: true,
          severity: "success",
          msg: "Successfully add one to cart",
        });
      } else {
        props.setAlert({
          open: true,
          severity: "error",
          msg: res.message,
        });
      }
    }
  };

  return (
    <React.Fragment>
      <TableRow className={classes.root}>
        <TableCell className={classes.tablecell} align="left">
          <Link onClick={() => history("/book/" + row.book_id)}>
            {row.name}
          </Link>
        </TableCell>
        <TableCell className={classes.tablecell} align="left">
          {row.author}
        </TableCell>
        <TableCell className={classes.tablecell} align="left">
          {row.publishing_house}
        </TableCell>
        <TableCell className={classes.tablecell} align="right">
          {row.publishing_date}
        </TableCell>
        <TableCell className={classes.tablecell} align="right">
          {row.price}
        </TableCell>
        <TableCell className={classes.tablecell} align="right">
          {discount_text}
        </TableCell>
        <TableCell className={classes.tablecell} align="right">
          <IconButton
            color={"primary"}
            disabled={false}
            aria-label="add"
            id={row.book_id}
            className={classes.btn}
            onClick={handleAddCart}
          >
            <AddBoxIcon />
          </IconButton>
        </TableCell>
        {/* <TableCell className={classes.tablecell} align="right">
          <IconButton
            aria-label="add"
            // id={row.id + row.class}
            id={row._id}
            className={classes.btn}
            onClick={handleCommentBtn}
          >
            <CommentIcon />
          </IconButton>
        </TableCell> */}
      </TableRow>
    </React.Fragment>
  );
}

function BookTable(props) {
  const useStyle = makeStyles((theme) => ({
    firstRowCell: {
      paddingLeft: theme.spacing(1),
      paddingRight: theme.spacing(1),
      paddingTop: theme.spacing(2),
      paddingBottom: theme.spacing(2),
      textAlign: "center",
    },
    modal: {
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
    },
    paper: {
      backgroundColor: theme.palette.background.paper,
      border: "2px solid #000",
      boxShadow: theme.shadows[5],
      padding: theme.spacing(2, 4, 3),
      width: "90%",
      height: "90%",
      overflow: "scroll",
    },
  }));

  const [page, setPage] = useState(0);
  const [books, setBooks] = useState([]);
  const rowsPerPage = 20;
  const attributes = [
    "name",
    "author",
    "publishing_house",
    "publishing_date",
    "price",
    "discount",
    "add to cart",
  ];

  useEffect(async () => {
    let listbooks = await listBook();
    if (listbooks.message === "Success") {
      setBooks(listbooks.data);
    }
    window.scrollTo(0, 0);
  }, [page]);

  const handleChangePage = (event, newPage) => {
    window.scroll(0, 0);
    setPage(newPage);
  };

  const classes = useStyle();
  return (
    <>
      <TableContainer component={Paper}>
        <Table aria-label="collapsible table">
          <TableHead>
            <TableRow>
              {/* <TableCell style={{ width: "6%" }} /> */}
              <TableCell
                align="left"
                className={classes.firstRowCell}
                style={{ width: "10%" }}
              >
                {" "}
                {attributes[0]}{" "}
              </TableCell>
              <TableCell
                align="left"
                className={classes.firstRowCell}
                style={{ width: "5%" }}
              >
                {" "}
                {attributes[1]}
              </TableCell>
              <TableCell
                // component="th"
                className={classes.firstRowCell}
                scope="row"
                style={{ width: "5%" }}
              >
                {attributes[2]}
              </TableCell>
              <TableCell
                align="left"
                className={classes.firstRowCell}
                style={{ width: "6%" }}
              >
                {attributes[3]}
              </TableCell>
              <TableCell
                align="left"
                className={classes.firstRowCell}
                style={{ width: "4.5%" }}
              >
                {attributes[4]}
              </TableCell>
              <TableCell
                align="right"
                className={classes.firstRowCell}
                style={{ width: "4.5%" }}
              >
                {attributes[5]}
              </TableCell>
              <TableCell
                align="right"
                className={classes.firstRowCell}
                style={{ width: "4.5%" }}
              >
                {attributes[6]}
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {books
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((book) => (
                <Row row={book} user={props.user} setAlert={props.setAlert} />
              ))}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[20]}
        component="div"
        count={books.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onChangePage={handleChangePage}
      />
    </>
  );
}

export default BookTable;
