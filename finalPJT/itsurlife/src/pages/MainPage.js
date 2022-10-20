import Footer from "../components/Footer";
import Navbar from "../components/Navbar";
import { useState, useEffect } from "react";
import axios from "axios";
import styled from "@emotion/styled";
import theme from "../styles/theme";

const MainPage = () => {
  const [lodgingInfo, setLodgingInfo] = useState([]);
  const fetchData = async () => {
    const response = await axios.get(
      "https://2bd94f30-be46-4031-b0dc-c5cc936e66e4.mock.pstmn.io/v1/home",
    );
    await console.log(response.data);
    setLodgingInfo(response.data);
  };
  useEffect(() => {
    fetchData();
  }, []);
  return (
    <>
      <Navbar />
      <ListBox>
        {lodgingInfo.map(lodging => {
          return (
            <ImgBox key={lodging.id} first_img={lodging.id === 1}>
              <img className="mainImg" src={lodging.image} alt={lodging.name} />
            </ImgBox>
          );
        })}
      </ListBox>
      <Footer />
    </>
  );
};
const ImgBox = styled.div`
  width: 337px;
  height: 225px;
  margin-right: 78px;
  margin-left: ${({ first_img }) => (first_img ? "130px" : "0px")};
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  border-radius: 25px;
  overflow: hidden;
  & > .mainImg {
    width: 337px;
    height: 225px;
    object-fit: cover;
  }
`;

const ListBox = styled.div`
  margin-top: 14px;
  margin-bottom: 65px;
  width: 1920px;
  height: 269px;
  display: block-flex;
  flex-direction: row;
  align-items: center;
  box-shadow: 0px 2px 4px #edece3, inset 0px 2px 4px #edece3;
  overflow: scroll;
  white-space: nowrap;
  &::-webkit-scrollbar {
    display: none;
  }
`;

export default MainPage;
