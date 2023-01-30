"use strict";

let mapping, firstDate;

class PureDate {
  constructor(date) {
    const dateCopy = new Date(date);
    dateCopy.setHours(0, 0, 0, 0);
    this.date = dateCopy;
  }

  get printDate() {
    const { date } = this;
    return (
      date.getFullYear() +
      "-" +
      ("0" + (date.getMonth() + 1)).slice(-2) +
      "-" +
      ("0" + date.getDate()).slice(-2)
    );
  }

  get nyaDate() {
    const { date } = this;
    const idx = Math.round((date - firstDate) / (1000 * 60 * 60 * 24));
    return mapping[idx].nya;
  }

  get nyaPrintDate() {
    const { nyaDate } = this;
    let count = 0;
    return (
      nyaDate.replace(
        /\//g,
        () => ["\u202f年\u202f", "\u202f星\u202f", "\u202f月\u202f"][count++]
      ) + "\u202f日"
    );
  }
}

const getDayOfWeekFromDateString = (dateString) => {
  const date = new Date(dateString);
  return date.getUTCDay();
};

const buildCalendarData = (pureDate) => {
  const { date } = pureDate;

  const idx = Math.round((date - firstDate) / (1000 * 60 * 60 * 24));
  let leftIdx = idx;
  let rightIdx = idx;
  const nyaDate = mapping[idx].nya;

  const nyaDateToMonth = (nyaDate) => nyaDate.split("/")[2];
  const nyaDateToDay = (nyaDate) => nyaDate.split("/")[3];
  const nyaMonth = nyaDateToMonth(nyaDate);

  // Extend to the whole month
  while (nyaDateToMonth(mapping[leftIdx - 1].nya) === nyaMonth) leftIdx--;
  while (nyaDateToMonth(mapping[rightIdx + 1].nya) === nyaMonth) rightIdx++;

  // Extend to full weeks
  const leftIdxExtended =
    leftIdx -
    ((getDayOfWeekFromDateString(mapping[leftIdx].gregorian) + 6) % 7);
  const rightIdxExtended =
    rightIdx +
    ((7 - getDayOfWeekFromDateString(mapping[rightIdx].gregorian)) % 7);

  let pointer = leftIdxExtended;
  const res = [];
  // console.log(leftIdx, rightIdxExtended, nyaMonth);

  while (pointer <= rightIdxExtended) {
    const week = [];
    for (let i = pointer; i < pointer + 7; i++)
      week.push({
        nyaDay: nyaDateToDay(mapping[i].nya),
        gregorian: mapping[i].gregorian.slice(5),
        iso: mapping[i].gregorian,
        isExtended: !(leftIdx <= i && i <= rightIdx),
        isCurrent: i === idx,
      });
    pointer += 7;
    res.push(week);
  }

  return res;
};

const renderDate = (pureDate) => {
  document.getElementById("nya-date").innerText = pureDate.nyaDate;

  const calendarData = buildCalendarData(pureDate);

  // HTML

  const fragment = document.createDocumentFragment();

  const title_div = document.createElement("div");
  title_div.classList.add("week-days");

  const title_span_0 = document.createElement("span");
  const title_span_1 = document.createElement("span");
  const title_span_2 = document.createElement("span");
  const title_span_3 = document.createElement("span");
  const title_span_4 = document.createElement("span");
  const title_span_5 = document.createElement("span");
  const title_span_6 = document.createElement("span");

  title_span_0.innerText = "月";
  title_span_1.innerText = "火";
  title_span_2.innerText = "水";
  title_span_3.innerText = "木";
  title_span_4.innerText = "金";
  title_span_5.innerText = "土";
  title_span_6.innerText = "日";

  title_div.appendChild(title_span_0);
  title_div.appendChild(title_span_1);
  title_div.appendChild(title_span_2);
  title_div.appendChild(title_span_3);
  title_div.appendChild(title_span_4);
  title_div.appendChild(title_span_5);
  title_div.appendChild(title_span_6);

  fragment.appendChild(title_div);

  // content

  calendarData.forEach((line) => {
    const div = document.createElement("div");
    div.classList.add("week");
    line.forEach(({ nyaDay, gregorian, iso, isExtended, isCurrent }) => {
      const span = document.createElement("span");

      span.addEventListener("click", () => {
        const pureDate = new PureDate(new Date(iso));
        document.getElementById("calendar-input").value = pureDate.printDate;
        renderDate(pureDate);
      });

      if (isExtended) span.classList.add("extended");
      if (isCurrent) span.classList.add("active");

      const innerSpan0 = document.createElement("span");
      innerSpan0.innerText = nyaDay;
      innerSpan0.classList.add("nya");

      const innerSpan1 = document.createElement("span");
      innerSpan1.innerText = gregorian;
      innerSpan1.classList.add("gregorian");

      span.appendChild(innerSpan0);
      span.appendChild(innerSpan1);
      div.appendChild(span);
    });
    fragment.appendChild(div);
  });

  const outputArea = document.getElementById("output-area");
  outputArea.innerHTML = "";
  outputArea.appendChild(fragment);
};

const loadData = async () => {
  const request = await fetch("dates.txt");
  const response = await request.text();
  mapping = response
    .trimEnd()
    .split("\n")
    .map((line) => {
      const [a, b] = line.split("\t");
      return { gregorian: a, nya: b };
    });
  firstDate = new Date(mapping[0].gregorian);

  const pureDate = new PureDate(new Date());
  document.getElementById("calendar-input").value = pureDate.printDate;
  renderDate(pureDate);
};

const handleOnChange = () => {
  const dateString = document.getElementById("calendar-input").value;
  const pureDate = new PureDate(new Date(dateString));
  document.getElementById("calendar-input").value = pureDate.printDate;
  renderDate(pureDate);
};

document.addEventListener("DOMContentLoaded", () => {
  loadData();
});
