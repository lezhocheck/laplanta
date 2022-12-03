import React from 'react';
import {RiPlantLine} from 'react-icons/ri';
import {AiOutlineHome, AiOutlineMail, AiOutlinePhone} from 'react-icons/ai';
import { MDBFooter, MDBContainer, MDBRow, MDBCol} from 'mdb-react-ui-kit';
import {BsFacebook, BsInstagram, BsTelegram, BsGithub, BsTwitter} from 'react-icons/bs';
import {useTranslation} from 'react-i18next';

const Footer = () => {
    const {t} = useTranslation();

    return (
        <MDBFooter bgColor="dark" className="text-center text-lg-start text-muted">
            <section className="d-flex justify-content-center justify-content-lg-between p-4 border-bottom">
                <div className="me-5 d-none d-lg-block">
                    <span>{t("footer_get_connected")}</span>
                </div>
                <div>
                    <a href='#!' className='me-4 text-reset'><BsFacebook size={30}/></a>
                    <a href='#!' className='me-4 text-reset'><BsInstagram size={30}/></a>
                    <a href='#!' className='me-4 text-reset'><BsTelegram size={30}/></a>
                    <a href='#!' className='me-4 text-reset'><BsGithub size={30}/></a>
                    <a href='#!' className='me-4 text-reset'><BsTwitter size={30}/></a>
                </div>
            </section>
            <section>
                <MDBContainer className="text-center text-md-start mt-5">
                    <MDBRow className="mt-3">
                        <MDBCol md="3" lg="4" xl="3" className="mx-auto mb-4">
                            <h6 className="text-uppercase fw-bold mb-4">
                                <RiPlantLine size={30}/>
                                <span> Laplanta</span>
                            </h6>
                            <p>
                                {t("footer_desc")}
                            </p>
                        </MDBCol>
                        <MDBCol md="2" lg="2" xl="2" className="mx-auto mb-4">
                            <h6 className="text-uppercase fw-bold mb-4">{t("footer_benefits")}</h6>
                            <p><a href="#!" className="text-reset">{t("footer_analytics")}</a></p>
                            <p><a href="#!" className="text-reset">{t("footer_autonomy")}</a></p>
                            <p><a href="#!" className="text-reset">{t("footer_cheapness")}</a></p>
                        </MDBCol>
                        <MDBCol md="3" lg="2" xl="2" className="mx-auto mb-4">
                            <h6 className="text-uppercase fw-bold mb-4">{t("footer_useful_links")}</h6>
                            <p><a href="#!" className="text-reset">{t("footer_order")}</a></p>
                            <p><a href="#!" className="text-reset">{t("profile")}</a></p>
                            <p><a href="#!" className="text-reset">{t("help")}</a></p>
                            <p><a href="#!" className="text-reset">{t("about_us")}</a></p>
                        </MDBCol>
                        <MDBCol md="4" lg="3" xl="3" className="mx-auto mb-md-0 mb-4">
                            <h6 className="text-uppercase fw-bold mb-4">{t("contacts")}</h6>
                            <p><AiOutlineHome size={20}/> {t("address")}</p>
                            <p><AiOutlineMail size={20}/> info@laplanta.com</p>
                            <p><AiOutlinePhone size={20}/> +380 (68) 000-00-00</p>
                            <p><AiOutlinePhone size={20}/> +380 (99) 111-11-11</p>
                        </MDBCol>
                    </MDBRow>
                </MDBContainer>
            </section>
            <div className="text-center p-4" style={{ backgroundColor: "rgba(0, 0, 0, 0.05)" }}>
                <span>© 2022 Copyright </span>
                <a className="text-reset fw-bold" href="http://localhost:3000/">laplanta.com</a>
            </div>
        </MDBFooter>
    );
}

export default Footer;