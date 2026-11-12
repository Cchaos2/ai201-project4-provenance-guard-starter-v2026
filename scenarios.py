"""
What my test runs. <- UNIT 8, MILESTONE 3

`run_eval.py` runs every scenario below three times. Each one says which of my
five criteria (criteria.md) it tests.

    criterion 1  my own writing             -> "c1 own writing"
    criterion 2  AI vs human score gap      -> "c2 AI set" + "c2 human set"
    criterion 3  every label reachable      -> "c3 label coverage"
    criterion 4  the appeal path            -> run_extra_checks.py (needs /appeal)
    criterion 5  bad input gets a 400       -> "c5 bad input" here (status codes),
                                               and run_extra_checks.py (error +
                                               message fields, /ping afterwards)

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you.

    "bodies"  a list of whole request bodies, sent exactly as written. Used when
              the malformed request IS the point.
"""

import json
from pathlib import Path

_SAMPLES = Path(__file__).parent / "samples"


def _sample(name: str) -> str:
    """The text of one file in samples/, so criterion 3 uses the same inputs
    as the Unit 7 label table."""
    return json.loads((_SAMPLES / f"{name}.json").read_text(encoding="utf-8"))["text"]


# ── Criterion 1 ── ten pieces I wrote myself, each at least 100 words ────────
# All ten come from a course report I wrote alone in 2025 (classifying the
# structural type of buildings with supervised and semi-supervised learning).
# Edits: PDF line breaks joined, words split by line breaks rejoined, section
# headings and citation markers removed (except [4] in piece 2, where removing
# it breaks the sentence). My wording is unchanged, typos included.
MY_WRITING = [
    # piece 1 (175 words)
    "The western part of the United States, like other countries located along the Pacific Ocean Ring of Fire, is known for its high seismicity. One of the initiatives developed to address this risk is the Rapid Visual Screening (RVS) method. This method aims to identify and select buildings at higher risk to be evaluated later with more detailed resources. To perform this task, FEMA has developed a detailed Handbook that allows qualified personnel to complete a collection form with information about the building. Once the form is filled out, a score can be obtained and reported to authorities to guide further action. This process is designed to take little time; however, it still requires a considerable amount of economic and human resources. Thus, it would be highly beneficial if at least part of the form could be automated. One of the first tasks the evaluator must perform is to identify the structural type of the building (e.g., concrete, steel, masonry, wood, etc.). Computer vision and deep learning techniques present and opportunity to automate this task.",
    # piece 2 (102 words)
    "Previous work has been conducted using supervised learning, achieving 64% accuracy in identifying the structural types of buildings. However, serious methodological flaws have been identified, such as performing data splitting after data augmentation. This research follows a robust methodology and applies both supervised and semi-supervised learning to classify the structural system of buildings. The Dataset used in this work was obtained from [4], and consists of 6200 pictures. The pictures include houses and buildings from different countries and cover eight structural types. The dataset was divided into 70% for training, 15% for validation, and 15% for testing, as shown in Table I.",
    # piece 3 (128 words)
    "The images were available in three formats: PNG, JPG, and JPEG, and exhibited a wide range of sizes. Most of them were 150×150 or 224×224 pixels, although many other dimensions were also present. In addition, the resolution varied considerably, with file sizes ranging from 10 kB to 100 kB. These variations introduced several challenges for the classification process. To address these issues, all images were converted to RGB format (removing the alpha channel in PNG files) and subsequently resized and cropped to a standard size, which varied depending on the model used, as indicated in Table II. Finally, to improve model performance, all images were normalized using the ImageNet statistics (mean and standard deviation). It was observed that normalization led to better results, particularly when applying transfer learning.",
    # piece 4 (164 words)
    "Data augmentation was employed to improve the robustness and generalization capability of the models. Over the years, data augmentation has consistently proven to be an effective method for reducing overfitting. In the case of supervised learning, data augmentation was applied exclusively to the training set. The transformations included a random crop after applying a zoom between 80% and 100% of the original image size, along with a random horizontal flip (see Fig. 1). For unsupervised learning, the data augmentation was slightly more aggressive, including a zoom between 75% and 100%, random cropping, random color jittering, and random conversion to grayscale (applied with a 7.5% probability). Examples of the augmentation applied are shown in Fig. 3. As in the supervised case, it is important that the data augmentation remains moderate. If the transformations are too aggressive, the model may fail to learn fundamental representations of the image. In particular, color information can sometimes provide subtle cues about the material and structural system of the building.",
    # piece 5 (153 words)
    "Several Convolutional Neural Networks (CNNs) were evaluated for the classification task. The first model was a custom architecture consisting of four convolutional layers with batch normalization and ReLU activation, followed by max pooling and adaptive average pooling to extract features. This model was developed from scratch and achieved good results on the CIFAR-10 dataset, obtaining 86.5% test accuracy. For the other models, transfer learning was applied. In this approach, a pretrained model was taken and adapted for the classification task by fine-tuning some of its final layers. Transfer learning has been successfully applied across various fields and tasks. The models selected for transfer learning were: Resnet-18, Resnet-50, VGG-16, and InceptionV3. In general, all layers were frozen except for the last block of layers, which were fine-tuned to improve performance (specifically, last residual block and the final fully connected layer for ResNet; classifier layers for VGG-16; and final and auxiliary classification heads for InceptionV3).",
    # piece 6 (107 words)
    "A custom dataset was created, as previously mentioned, to generate pairs of augmented views. A SimCLR model was then used, with a ResNet-18 backbone and a projection head. For the pretraining phase, the criterion applied was the Normalized Temperature-Scaled Cross-Entropy Loss (NT-Xent). Once the model was pretrained, a new fully connected layer was added, and varying percentages of labeled data were used to evaluate the results. The percentage of labels tested ranged from 1% to 99%. The main metric used to evaluate model performance was average accuracy. This was calculated by counting the total number of correctly classified buildings and dividing by the total number of buildings.",
    # piece 7 (141 words)
    "Unlike machine learning engineers or data scientists, civil engineers often do not have access to large clusters of GPUs or high-end graphics cards. For this reason, all experiments were carried out using a T4 GPU with 16 GB of memory in the Google Colab environment, at an approximate cost of $0.15 USD per hour. This makes the T4 a very good option for working with small to medium-sized datasets, provided that the maximum batch size and image size are managed carefully to avoid out-of-memory errors. Several experiments were conducted. In the following section, multiple tables and figures are presented to show the results. The first experiment compared the improvement in accuracy when fine-tuning only the final fully connected layer versus fine-tuning the last block of layers. As shown in Table III, the results were considerably better when fine-tuning the last block.",
    # piece 8 (208 words)
    "The next evaluation focused on comparing different models. Five models were tested: one trained from scratch and four using transfer learning. The model trained from scratch performed the worst and was significantly behind the others. Although this model achieved good performance on the CIFAR-10 test set (>86% accuracy), its results for this task were poor. This highlights the difficulty of training a model from scratch for specialized tasks and shows that, in most cases, using a pretrained model with transfer learning produces better results. The other models all achieved better and relatively similar performance, with test accuracies ranging between 67% and 70%. Considering the characteristics of the dataset — a relatively small number of images, varying sizes and resolutions, class imbalance, and the inherent difficulty of the task (in some cases, even experienced civil engineers would need to enter the building to correctly identify the structural type based only on the facade) — these results are quite reasonable. It is also important to highlight that when working with a small dataset, using a larger model with more parameters does not necessarily guarantee better performance. In fact, larger models may be more prone to overfitting. This could help explain why ResNet-18 achieved the best results (by a small margin).",
    # piece 9 (199 words)
    "As mentioned earlier, this dataset was originally used in another study, where the same models (ResNet-18, VGG-16, and InceptionV3) were evaluated for the same classification task. As shown in Table V, the results obtained in this research are consistently better across all models, in some cases achieving improvements of more than 35%. To better analyze which structural types were correctly predicted and where the models failed, a confusion matrix was generated (Fig. 4). It can be observed that, in general, the structural types with higher accuracy correspond to those with more training data, such as concrete (C), steel (S), unreinforced masonry (URM), and wood (W). Conversely, the worst results are associated with building types that had fewer examples in the dataset, such as reinforced masonry (RM) and non-FEMA buildings (NF). This highlights the importance of collecting more curated data, particularly for underrepresented structural types, to achieve better performance. A special case is observed with manufactured houses: although this class had fewer samples than others, it achieved the highest accuracy (65 out of 79 houses correctly classified). This result is likely due to the distinct structural characteristics of manufactured houses, which make them more easily distinguishable from other building types.",
    # piece 10 (169 words)
    "Finally, six semi-supervised learning experiments were performed. The objective was to determine the minimum percentage of labeled data needed to achieve reasonable results. As shown in Fig. 5 and Table VII, even with only 1% of the labels, the model achieved an accuracy of approximately 44%. This result confirms the strength of the contrastive learning process and the quality of the feature representations generated by SimCLR: even with a minimal quantity of labels, the model can classify many additional images correctly. It is also observed that while accuracy improves as more labels are used, the gains plateau around 20–30% labeled data. This behavior highlights a known limitation of semi-supervised learning: the pretraining task in SimCLR is based on instance discrimination, which does not perfectly align with the goal of classification by structural type. This research explored the classification of structural systems in buildings using supervised and semi-supervised learning approaches. A robust methodology was followed to address several limitations identified in previous studies, particularly in data handling and evaluation protocols.",
]


# ── Criterion 2 ── five clearly-AI texts ─────────────────────────────────────
# Generated by a chatbot (Claude) from a one-line prompt each, not edited.
# The prompts, in order:
#   1. "Write a short paragraph about the benefits of regular exercise."
#   2. "Write a paragraph explaining why sleep is important for students."
#   3. "Write a short paragraph about how remote work has changed offices."
#   4. "Write a paragraph on the importance of recycling."
#   5. "Write a short paragraph about why learning a second language is valuable."
AI_SET = [
    "Regular exercise offers a wide range of benefits for both physical and mental "
    "health. Engaging in physical activity strengthens the heart, improves "
    "circulation, and helps maintain a healthy weight. It also builds muscle and "
    "bone strength, which becomes increasingly important as we age. Beyond the "
    "physical advantages, exercise has a powerful effect on mental well-being. It "
    "releases endorphins, which can reduce stress and improve mood, and it has been "
    "shown to lower the risk of anxiety and depression. Regular activity can also "
    "improve sleep quality and boost energy levels throughout the day. Even moderate "
    "exercise, such as a brisk thirty-minute walk most days of the week, can make a "
    "meaningful difference. Ultimately, making exercise a consistent part of your "
    "routine is one of the most effective investments you can make in your "
    "long-term health.",

    "Sleep plays a crucial role in the academic success and overall well-being of "
    "students. During sleep, the brain consolidates memories and processes the "
    "information learned throughout the day, which makes adequate rest essential "
    "for effective learning. Students who consistently get enough sleep tend to "
    "have better concentration, sharper problem-solving skills, and improved "
    "academic performance. In contrast, sleep deprivation can impair attention, "
    "slow reaction times, and make it harder to retain new material. Lack of sleep "
    "is also linked to increased stress, irritability, and a weakened immune "
    "system. Despite these risks, many students sacrifice sleep to study late or "
    "keep up with social commitments. By prioritizing a regular sleep schedule and "
    "aiming for seven to nine hours each night, students can support both their "
    "learning and their long-term health.",

    "Remote work has fundamentally transformed the way offices operate and how "
    "employees approach their jobs. As more companies have adopted flexible "
    "arrangements, traditional office spaces have shifted from places of daily "
    "routine to hubs for collaboration and connection. Many organizations have "
    "reduced their physical footprint, opting for smaller offices or shared "
    "workspaces to cut costs. At the same time, technology has become central to "
    "everyday work, with video conferencing, cloud-based tools, and instant "
    "messaging platforms enabling teams to stay connected across locations. This "
    "shift has offered employees greater flexibility and eliminated long commutes, "
    "but it has also introduced new challenges, such as maintaining team culture "
    "and preventing feelings of isolation. Overall, remote work has prompted "
    "companies to rethink what an office is for and how work can be done most "
    "effectively.",

    "Recycling is an important practice that helps protect the environment and "
    "conserve valuable natural resources. By turning used materials such as paper, "
    "plastic, glass, and metal into new products, recycling reduces the need to "
    "extract and process raw materials. This, in turn, saves energy and lowers "
    "greenhouse gas emissions associated with manufacturing. Recycling also "
    "decreases the amount of waste sent to landfills and incinerators, which can "
    "pollute the air, soil, and water. In addition, the recycling industry creates "
    "jobs and supports local economies. While recycling alone cannot solve every "
    "environmental challenge, it is a simple and effective way for individuals and "
    "communities to make a positive impact. By recycling consistently and "
    "correctly, we can all contribute to a cleaner and more sustainable future for "
    "generations to come.",

    "Learning a second language is a valuable skill that offers numerous personal, "
    "professional, and cognitive benefits. On a personal level, it allows "
    "individuals to connect with people from different cultures, travel more "
    "confidently, and gain a deeper appreciation for other ways of life. "
    "Professionally, being bilingual can open doors to new career opportunities, as "
    "many employers value candidates who can communicate with diverse clients and "
    "colleagues. Research has also shown that learning a new language can enhance "
    "cognitive abilities, including memory, problem-solving, and multitasking "
    "skills. Additionally, studying another language often improves understanding "
    "of one's own native language. Whether for work, travel, or personal growth, "
    "learning a second language is an enriching experience that broadens "
    "perspectives and creates meaningful connections across the world.",
]


SCENARIOS = [
    {
        "name": "c1 own writing",
        "criterion": 1,
        "texts": MY_WRITING,
    },
    {
        "name": "c2 AI set",
        "criterion": 2,
        "texts": AI_SET,
    },
    {
        # The human half of criterion 2: the first five of my own pieces.
        "name": "c2 human set",
        "criterion": 2,
        "texts": MY_WRITING[:5],
    },
    {
        # The Unit 7 label-table inputs: two expected per label.
        "name": "c3 label coverage",
        "criterion": 3,
        "texts": [
            _sample("ai_1"), _sample("ai_2"),          # expected: ai
            _sample("human_1"), _sample("human_3"),    # expected: human
            _sample("unsure_1"), _sample("unsure_2"),  # expected: unsure
        ],
    },
    {
        # Each body has its own creator_id, so the rate limiter (5/minute per
        # creator) never answers instead of my route.
        "name": "c5 bad input",
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_bad_missing"},                  # no text field
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "   \n\t  ", "creator_id": "eval_bad_space"},
            {"text": None, "creator_id": "eval_bad_null"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )

    # Criterion 1 says "each at least 100 words".
    for j, text in enumerate(MY_WRITING, 1):
        if not str(text).startswith("REPLACE ME") and len(str(text).split()) < 100:
            problems.append(
                f"MY_WRITING piece {j} has {len(str(text).split())} words — "
                f"criterion 1 needs at least 100"
            )
    return problems