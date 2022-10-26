import styled from "@emotion/styled";
import theme from "../styles/theme";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { useLocation } from "react-router-dom";
const SearchPage = () => {
  const a = useLocation;
  const data = a.state;
  console.log(data);
  return (
    <>
      <Navbar />
      <div>검색페이지</div>
      <Footer />
    </>
  );
};
export default SearchPage;
