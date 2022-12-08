import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import ListGroup from 'react-bootstrap/ListGroup';
import Col from 'react-bootstrap/Col';
import {AiOutlineInfoCircle, AiOutlineCalendar, AiOutlineBorderlessTable} from 'react-icons/ai';
import {MdDriveFileRenameOutline} from 'react-icons/md';
import useAxiosPrivate from '../../hooks/useAxiosPrivate';
import {useState, useEffect} from 'react';
import Records from './Records';
import { Accordion } from 'react-bootstrap';
import {useTranslation} from 'react-i18next';

const Sensor = ({sensor, plantId}) => {
    const {t} = useTranslation();
    const axiosPrivate = useAxiosPrivate();
    const [records, setRecords] = useState();

    useEffect(() => {
        let isMounted = true;
        const controller = new AbortController();
        const getRecords = async () => {
            try {
                const response = await axiosPrivate.get(`/plant/${plantId}/records`, {
                    signal: controller.signal
                });
                isMounted && setRecords(response.data?.msg?.records);
            } catch(e) {
                console.error(e);
            }
        }

        getRecords();

        return () => {
            isMounted = false;
            controller.abort();
        }
    }, []);


    return (
        <Container>
            <h3>{t("plant_name") + ": " + sensor?.name}</h3>
            <ListGroup>
                <ListGroup.Item>
                    <Row>
                        <Col sm="3" className="d-flex justify-content-start align-items-center gap-1">
                            <AiOutlineBorderlessTable size={20}/>
                            <span className="p">Id</span>
                        </Col>
                        <Col sm="9" className="d-flex justify-content-start align-items-center">
                            <span className="p text-muted">{sensor?._id}</span>
                        </Col>
                    </Row>
                </ListGroup.Item>
                <ListGroup.Item>
                    <Row>
                        <Col sm="3" className="d-flex justify-content-start align-items-center gap-1">
                            <MdDriveFileRenameOutline size={20}/>
                            <span className="p">{t("type")}</span>
                        </Col>
                        <Col sm="9" className="d-flex justify-content-start align-items-center">
                            <span className="p text-muted">{sensor?.type}</span>
                        </Col>
                    </Row>
                </ListGroup.Item>
                <ListGroup.Item>
                    <Row>
                        <Col sm="3" className="d-flex justify-content-start align-items-center gap-1">
                            <AiOutlineCalendar size={20}/>
                            <span className="p">{t("added_date")}</span>
                        </Col>
                        <Col sm="9" className="d-flex justify-content-start align-items-center">
                            <span className="p text-muted">{sensor?.added_date}</span>
                        </Col>
                    </Row>
                </ListGroup.Item>
                <ListGroup.Item>
                    <Row>
                        <Col sm="3" className="d-flex justify-content-start align-items-center gap-1">
                            <AiOutlineCalendar size={20}/>
                            <span className="p">{t("last_data_sent")}</span>
                        </Col>
                        <Col sm="9" className="d-flex justify-content-start align-items-center">
                            <span className="p text-muted">{sensor?.last_data_sent}</span>
                        </Col>
                    </Row>
                </ListGroup.Item>
                <ListGroup.Item>
                    <Row>
                        <Col sm="3" className="d-flex justify-content-start align-items-center gap-1">
                            <AiOutlineInfoCircle size={20}/>
                            <span className="p">{t("status")}</span>
                        </Col>
                        <Col sm="9" className="d-flex justify-content-start align-items-center">
                            <span className="p text-muted">{sensor?.status}</span>
                        </Col>
                    </Row>
                </ListGroup.Item>
            </ListGroup>
            <br/>
            <Accordion flush alwaysOpen>
                <Accordion.Item eventKey="0">
                    <Accordion.Header>{t("records")}</Accordion.Header>
                    <Accordion.Body>
                        <Records records={records} sensorId={sensor?._id}/>
                    </Accordion.Body>
                </Accordion.Item>
            </Accordion>
        </Container>
    );
}

export default Sensor;