import BootstrapTable from 'react-bootstrap-table-next';
import Spinner from 'react-bootstrap/Spinner';
import { Button, ButtonGroup } from 'react-bootstrap';
import { Line } from 'react-chartjs-2';
import { useState } from 'react';
import { Chart, registerables } from 'chart.js';
import {useTranslation} from 'react-i18next';

Chart.register(...registerables);

const Records = ({records, sensorId}) => {
    const {t} = useTranslation();
    const [section, setSection] = useState('table');

    const columns = [
        {
            dataField: 'prediction',
            text: t("predicted"),
            sort: true
        },
        {
            dataField: 'mean',
            text: t("means"),
            sort: true
        },
        {
            dataField: 'std_dev',
            text: t("std_dev"),
            sort: true
        },
        {
            dataField: 'variance',
            text: t("variance"),
            sort: true
        },
        {
            dataField: 'date',
            text: t("measure_date"),
            sort: true
        }
    ];

    const getData = () => {
        return records.filter(x => x.sensor_id === sensorId);
    }

    return (
        <div>
            <ButtonGroup className="mb-2 d-flex gap-1" style={{width: '70%'}}>
                <Button onClick={() => setSection('table')}>{t("table")}</Button>
                <Button onClick={() => setSection('pred')}>{t("graph_pred")}</Button>
                <Button onClick={() => setSection('stats')}>{t("graph_stats")}</Button>
            </ButtonGroup>
            {
                records && records.length > 0 
                ?
                <div>
                    {
                        (() => {
                            if (section === 'table') {
                                return (
                                    <BootstrapTable
                                        bootstrap4 
                                        keyField="_id"
                                        data={getData()}
                                        columns={columns}
                                        bordered={false}
                                    />
                                );
                            } else if (section === 'pred') {
                                return (
                                    <Line
                                        datasetIdKey='id'
                                        data={{
                                                labels: getData().map(x => x.date),
                                                datasets: [
                                                    {
                                                        id: 1,
                                                        label: t("predicted"),
                                                        data: getData().map(x => x.prediction),
                                                    },
                                                    {
                                                        id: 2,
                                                        label: t("measured"),
                                                        data: getData().slice(0, -1).map(x => x.values),
                                                    }
                                                ]
                                            }
                                        }
                                        options = {
                                            {
                                                scales: {
                                                    x: {
                                                        display: false
                                                    }
                                                }  
                                            }
                                        }
                                    />
                                );
                            } else {
                                return (
                                    <Line
                                        datasetIdKey='id'
                                        data={{
                                                labels: getData().map(x => x.date),
                                                datasets: [
                                                    {
                                                        id: 1,
                                                        label: t("means"),
                                                        data: getData().map(x => x.mean),
                                                    },
                                                    {
                                                        id: 2,
                                                        label: t("std_dev"),
                                                        data: getData().map(x => x.std_dev),
                                                    },
                                                    {
                                                        id: 3,
                                                        label: t("variance"),
                                                        data: getData().map(x => x.variance),
                                                    }
                                                ]
                                            }
                                        }
                                        options = {
                                            {
                                                scales: {
                                                    x: {
                                                        display: false
                                                    }
                                                }  
                                            }
                                        }
                                    />
                                );
                            }
                        })()
                    }
                </div>
                :
                <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading...</span>
                </Spinner>
            }
        </div>
    );
}

export default Records;