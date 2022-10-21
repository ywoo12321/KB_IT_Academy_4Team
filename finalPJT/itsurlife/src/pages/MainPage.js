import Footer from "../components/Footer";
import Navbar from "../components/Navbar";
import { useState, useEffect } from "react";
import axios from "axios";
import styled from "@emotion/styled";
import theme from "../styles/theme";
import { symbol } from "prop-types";

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
              <LodgingName>{lodging.name}</LodgingName>
              <LodgingImage src={lodging.image} alt={lodging.name} />
            </ImgBox>
          );
        })}
      </ListBox>
      <Footer />
    </>
  );
};
const LodgingName = styled.div`
  display: none;
  z-index: 99;
  position: absolute;
  font-family: ${theme.font_family.T};
  font-size: ${theme.font_size.h4};
  color: ${theme.color.whiteFont};
  top: 80%;
  left: 50%;
  transform: translate(-50%, -50%);
  cursor: pointer;
`;

const LodgingImage = styled.img`
  width: 337px;
  height: 225px;
  object-fit: cover;
  z-index: -10;
  cursor: pointer;
  &:hover {
    filter: brightness(0.4);
  }
`;
const ImgBox = styled.div`
  width: 337px;
  height: 225px;
  position: relative;
  margin-right: 78px;
  margin-left: ${({ first_img }) => (first_img ? "130px" : "0px")};
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  border-radius: 25px;
  overflow: hidden;
  & > .mainImg {
    position: relative;
    width: 337px;
    height: 225px;
    object-fit: cover;
  }
  &:hover {
    & > div {
      display: block;
    }
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
