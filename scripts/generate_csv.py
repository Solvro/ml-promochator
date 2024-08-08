import csv
import json
import os

data = [
    {
        "Supervisor's name": 'Jarosław Drapała',
        'interests': 'mathematical modelingdynamical systemsmachine learningexploratory data analysis',
        'research papers': {
            'Impairments of working memory in schizophrenia and bipolar disorder: the effect of history of psychotic symptoms and different aspects of cognitive task demands': 'Comparisons of cognitive impairments between schizophrenia (SZ) and bipolar disorder (BPD) have produced mixed results. We applied different working memory (WM) measures (Digit Span Forward and Backward, Short-delay and Long-delay CPT-AX, N-back) to patients with SZ (n = 23), psychotic BPD (n = 19) and non-psychotic BPD (n = 24), as well as to healthy controls (HC) (n = 18) in order to compare the level of WM impairments across the groups. With respect to the less demanding WM measures (Digit Span Forward and Backward, Short-delay CPT-AX), there were no between group differences in cognitive performance; however, with respect to the more demanding WM measures (Long-delay CPT-AX, N-back), we observed that the groups with psychosis (SZ, psychotic BPD) did not differ from one another, but performed poorer than the group without a history of psychosis (non-psychotic BPD). A history of psychotic symptoms may influence cognitive performance with respect to WM delay and load effects as measured by Long-delay CPT-AX and N-back tests, respectively. We observed a positive correlation of WM performance with antipsychotic treatment and a negative correlation with depressive symptoms in BPD and with negative symptoms in SZ subgroup. Our study suggests that WM dysfunctions are more closely related to a history of psychosis than to the diagnostic categories of SZ and BPD described by psychiatric classification systems.',
            'ADAPTIVE DECISION SUPPORT SYSTEM FOR AUTOMATIC PHYSICAL EFFORT PLAN GENERATION—DATA-DRIVEN APPROACH': "Mathematical models delivered using both expert knowledge and experimental data improve understanding of dynamic properties of the system under consideration. This is useful for different purposes, such as prediction, diagnosis, decision making, and system control. A data-driven approach has been found to be particularly useful in designing adaptive decision support systems. We demonstrate the usefulness of data-driven models in a custom application designed for sport training management. We have developed a system that makes use of expert knowledge together with measurement data (heart rate, electromyography, and acceleration) as well as environmental (Global Positioning System) in order to generate an optimal training plan. The system performs such tasks as modeling of the athlete's cardiovascular system, estimation of the athlete's parameters, and adaptation of the model to the athlete.",
        },
    },
    {
        "Supervisor's name": 'Krzysztof Brzostowski',
        'interests': 'nonlinear signal processingtime-frequency analysissparsity techniquessystem identificationdata fusion',
        'research papers': {
            'Two stage EMG onset detection method': 'Detection of the moment when a muscle begins to activate on the basis of EMG signal is important task for a number of biomechanical studies. In order to provide high accuracy of EMG onset detection, we developed novel method, that give results similar to that obtained by an expert. By means of this method, EMG is processed in two stages. The first stage gives rough estimation of EMG onset, whereas the second stage performs local, precise searching. The method was applied to support signal processing in biomechanical study concerning effect of body position on EMG activity and peak muscle torque stabilizing spinal column under static conditions.',
            'ADAPTIVE DECISION SUPPORT SYSTEM FOR AUTOMATIC PHYSICAL EFFORT PLAN GENERATION—DATA-DRIVEN APPROACH': "Mathematical models delivered using both expert knowledge and experimental data improve understanding of dynamic properties of the system under consideration. This is useful for different purposes, such as prediction, diagnosis, decision making, and system control. A data-driven approach has been found to be particularly useful in designing adaptive decision support systems. We demonstrate the usefulness of data-driven models in a custom application designed for sport training management. We have developed a system that makes use of expert knowledge together with measurement data (heart rate, electromyography, and acceleration) as well as environmental (Global Positioning System) in order to generate an optimal training plan. The system performs such tasks as modeling of the athlete's cardiovascular system, estimation of the athlete's parameters, and adaptation of the model to the athlete.",
        },
    },
    {
        "Supervisor's name": 'Dariusz Gąsior',
        'interests': 'virtual networksautonomic networksself-managed networks',
        'research papers': {
            'Pareto-optimal Nash equilibrium in capacity allocation game for self-managed networks': 'In this paper we introduce a capacity allocation game which models the problem of maximizing network utility from the perspective of distributed noncooperative agents. Motivated by the idea of self-managed networks, in the developed framework the decision-making entities are associated with individual transmission links, deciding on the way they split capacity among concurrent flows. An efficient decentralized algorithm is given for computing a strongly Pareto-optimal strategies, constituting a pure Nash equilibrium. Subsequently, we discuss the properties of the introduced game related to the Price of Anarchy and Price of Stability. The paper is concluded with an experimental study.',
            'An Algorithm for Rescheduling of Trains under Planned Track Closures': 'This work considered a joint problem of train rescheduling and closure planning. The derivation of a new train run schedule and the determination of a closure plan not only must guarantee the satisfaction of all the given constraints but also must optimize the number of accepted closures, the number of approved train runs, and the total time shift between the resultant and the original schedule. Presented is a novel nonlinear mixed integer optimization problem which is valid for a broad class of railway networks. A multi-level hierarchical heuristic algorithm is introduced due to the NP-hardness of the considered optimization problem. The algorithm is able, on an iterative basis, to jointly select closures and train runs, along with the derivation of a train schedule. Results obtained by the algorithm, launched for the conducted experiments, confirm its ability to provide acceptable and feasible solutions in a reasonable amount of time.',
        },
    },
    {
        "Supervisor's name": 'Grzegorz Filcek',
        'interests': 'Multiple Criteria OptimizationSupply NetworksComputer NetworksMathematical ModellingTransportation',
        'research papers': {
            'A heuristic algorithm for solving a Multiple Criteria Carpooling Optimization (MCCO) problem': 'The authors consider in this paper a carpooling optimization problem, which is formulated (based on their previous work) as a constrained multiple criteria decision-making problem. Different aspects and contradictory preferences of individual stakeholders/carpoolers (drivers and passengers), including: economic, comfort- and safety-oriented, and social are considered. The formulated problem is focused on the joint matching of carpoolers and planning their routes in order to maximize the utility of all travelers. To solve the problem, the authors develop a heuristic computational procedure that applies a problem-specific heuristic method (carpooler’s matching component) combined with a utility-based shortest path algorithm (routing component). The procedure aggregates all of the considered criteria by a weighted scaling function and then applies a greedy algorithm to generate most satisfactory routes for all of the',
        },
    },
]

csv_file = os.path.abspath('./data/data_csv_json.csv')


with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Supervisor's name", 'interests', 'research papers'])
    for item in data:
        writer.writerow(
            [
                item["Supervisor's name"],
                item['interests'],
                json.dumps(item['research papers']),
            ]
        )
