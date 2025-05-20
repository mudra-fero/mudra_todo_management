export const capitalize = (val) => {
    return String(val).charAt(0).toUpperCase() + String(val).slice(1);
}

export const removeUnderScore = (val) => {
    return String(val).replaceAll("_", " ");
}

export const removeUnderScoreAndCapitalize = (val) => {
    return capitalize(removeUnderScore(val));
}